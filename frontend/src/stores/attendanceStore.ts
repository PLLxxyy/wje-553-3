import { defineStore } from 'pinia';
import { attendanceApi } from '../api/attendance';
import type { Attendance, CourseAttendanceSummary, StudentAbsenceRank } from '../types/attendance';
export const useAttendanceStore = defineStore('attendance', {
  state: () => ({
    items: [] as Attendance[],
    courseSummaries: [] as CourseAttendanceSummary[],
    absenceRanking: [] as StudentAbsenceRank[],
  }),
  actions: {
    async fetch(params?: Record<string, string>) {
      this.items = await attendanceApi.list(params);
    },
    async changeStatus(id: string, status: Attendance['status']) {
      await attendanceApi.update(id, { status });
      await Promise.all([this.fetch(), this.fetchCourseSummary(), this.fetchAbsenceRanking()]);
    },
    async fetchCourseSummary(params?: Record<string, string>) {
      this.courseSummaries = await attendanceApi.getCourseSummary(params);
    },
    async fetchAbsenceRanking(params?: Record<string, string | number>) {
      this.absenceRanking = await attendanceApi.getAbsenceRanking(params);
    },
  },
});
