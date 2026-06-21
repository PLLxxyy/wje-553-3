import type { AttendanceStatus } from '../constants/enums';
export interface Attendance { id: string; course_id: string; student_id: string; course_name?: string; student_name?: string; date: string; status: AttendanceStatus; remark?: string; created_at: string; updated_at: string }
export interface CourseAttendanceSummary {
  course_id: string;
  course_name: string;
  total_records: number;
  present_count: number;
  absent_count: number;
  late_count: number;
  leave_count: number;
  pending_count: number;
  attendance_rate: number;
}
export interface StudentAbsenceRank {
  student_id: string;
  student_name: string;
  student_no: string;
  absent_count: number;
  late_count: number;
  total_absent: number;
  rank: number;
}
