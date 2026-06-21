<script setup lang="ts">
import { onMounted, ref } from 'vue'; import StatusTag from '../components/common/StatusTag.vue'; import { useAttendance } from '../hooks/useAttendance';
const { attendance, courseSummaries, absenceRanking, fetchAttendance, changeAttendanceStatus, fetchCourseSummary, fetchAbsenceRanking } = useAttendance();
const activeTab = ref('records');
onMounted(() => { fetchAttendance(); fetchCourseSummary(); fetchAbsenceRanking(); });
function getAttendanceRateColor(rate: number) {
  if (rate >= 90) return '#67c23a';
  if (rate >= 70) return '#e6a23c';
  return '#f56c6c';
}
</script>
<template>
<section class="page">
  <header>
    <h2>考勤管理</h2>
    <el-button v-permission="['ADMIN','TEACHER']" type="primary">一键全部出勤</el-button>
  </header>
  <el-tabs v-model="activeTab">
    <el-tab-pane label="考勤明细" name="records">
      <el-table :data="attendance">
        <el-table-column prop="course_name" label="课程"/>
        <el-table-column prop="student_name" label="学生"/>
        <el-table-column prop="date" label="日期"/>
        <el-table-column label="状态">
          <template #default="{row}"><StatusTag :status="row.status" type="attendance"/></template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="{row}">
            <el-button size="small" @click="changeAttendanceStatus(row.id,'PRESENT')" v-permission="['ADMIN','TEACHER']">出勤</el-button>
            <el-button size="small" @click="changeAttendanceStatus(row.id,'ABSENT')" v-permission="['ADMIN','TEACHER']">缺勤</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="课程汇总" name="summary">
      <el-table :data="courseSummaries">
        <el-table-column prop="course_name" label="课程"/>
        <el-table-column prop="total_records" label="总记录" width="100"/>
        <el-table-column prop="present_count" label="出勤" width="90"/>
        <el-table-column prop="absent_count" label="缺勤" width="90"/>
        <el-table-column prop="late_count" label="迟到" width="90"/>
        <el-table-column prop="leave_count" label="请假" width="90"/>
        <el-table-column prop="pending_count" label="待处理" width="100"/>
        <el-table-column label="出勤率" width="130">
          <template #default="{row}">
            <el-progress
              :percentage="row.attendance_rate"
              :color="getAttendanceRateColor(row.attendance_rate)"
              :stroke-width="10"
            />
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="缺勤排名" name="ranking">
      <el-table :data="absenceRanking">
        <el-table-column prop="rank" label="排名" width="80">
          <template #default="{row}">
            <span :style="{ fontWeight: row.rank <= 3 ? 'bold' : 'normal', color: row.rank <= 3 ? '#f56c6c' : '' }">
              {{ row.rank }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="student_no" label="学号" width="130"/>
        <el-table-column prop="student_name" label="学生"/>
        <el-table-column prop="absent_count" label="缺勤次数" width="110"/>
        <el-table-column prop="late_count" label="迟到次数" width="110"/>
        <el-table-column prop="total_absent" label="合计" width="100">
          <template #default="{row}">
            <span style="font-weight: bold; color: #f56c6c;">{{ row.total_absent }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>
</section>
</template>