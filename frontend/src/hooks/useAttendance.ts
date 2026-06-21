import { storeToRefs } from 'pinia';
import { useAttendanceStore } from '../stores/attendanceStore';
export function useAttendance() {
  const store = useAttendanceStore();
  const { items, courseSummaries, absenceRanking } = storeToRefs(store);
  return {
    attendance: items,
    courseSummaries,
    absenceRanking,
    fetchAttendance: store.fetch,
    changeAttendanceStatus: store.changeStatus,
    fetchCourseSummary: store.fetchCourseSummary,
    fetchAbsenceRanking: store.fetchAbsenceRanking,
  };
}
