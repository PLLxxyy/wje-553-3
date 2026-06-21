import { request } from '../utils/request';
import type { Attendance, CourseAttendanceSummary, StudentAbsenceRank } from '../types/attendance';
export const attendanceApi = {
  list: (params?: Record<string, string>) => request.get<unknown, Attendance[]>('/attendance', { params }),
  update: (id: string, payload: Partial<Attendance>) => request.patch<unknown, Attendance>('/attendance/' + id, payload),
  getCourseSummary: (params?: Record<string, string>) => request.get<unknown, CourseAttendanceSummary[]>('/attendance/summary/courses', { params }),
  getAbsenceRanking: (params?: Record<string, string | number>) => request.get<unknown, StudentAbsenceRank[]>('/attendance/ranking/absence', { params }),
};
