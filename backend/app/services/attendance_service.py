from fastapi import HTTPException
from sqlalchemy import func, case, desc
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.course import Course
from app.models.student import Student
from app.schemas.attendance_schema import AttendanceCreate, AttendanceUpdate, CourseAttendanceSummary, StudentAbsenceRank
from app.core.enums import AttendanceStatus
from .audit_service import audit_service

class AttendanceService:
    def list_attendance(self, db: Session, course_id: str | None = None, student_id: str | None = None):
        query = db.query(Attendance)
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        if student_id:
            query = query.filter(Attendance.student_id == student_id)
        return query.order_by(Attendance.date.desc()).all()

    def create_attendance(self, db: Session, payload: AttendanceCreate, user_id=None) -> Attendance:
        item = Attendance(**payload.model_dump())
        db.add(item); db.commit(); db.refresh(item)
        audit_service.log(db, "attendance.create", "Attendance", str(item.id), user_id=user_id, after_data=payload.model_dump(mode="json"))
        return item

    def update_attendance(self, db: Session, attendance_id: str, payload: AttendanceUpdate, user_id=None) -> Attendance:
        item = db.get(Attendance, attendance_id)
        if not item:
            raise HTTPException(status_code=404, detail="Attendance not found")
        before = {"status": item.status.value, "remark": item.remark}
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit(); db.refresh(item)
        audit_service.log(db, "attendance.update", "Attendance", str(item.id), user_id=user_id, before_data=before, after_data=payload.model_dump(exclude_unset=True, mode="json"))
        return item

    def get_course_summary(self, db: Session, course_id: str | None = None) -> list[CourseAttendanceSummary]:
        query = db.query(
            Attendance.course_id,
            Course.name.label('course_name'),
            func.count(Attendance.id).label('total_records'),
            func.sum(case((Attendance.status == AttendanceStatus.PRESENT, 1), else_=0)).label('present_count'),
            func.sum(case((Attendance.status == AttendanceStatus.ABSENT, 1), else_=0)).label('absent_count'),
            func.sum(case((Attendance.status == AttendanceStatus.LATE, 1), else_=0)).label('late_count'),
            func.sum(case((Attendance.status == AttendanceStatus.LEAVE, 1), else_=0)).label('leave_count'),
            func.sum(case((Attendance.status == AttendanceStatus.PENDING, 1), else_=0)).label('pending_count'),
        ).join(Course, Attendance.course_id == Course.id).group_by(Attendance.course_id, Course.name)
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        results = query.all()
        summaries = []
        for row in results:
            total = row.total_records
            present = row.present_count or 0
            attendance_rate = (present / total * 100) if total > 0 else 0.0
            summaries.append(CourseAttendanceSummary(
                course_id=row.course_id,
                course_name=row.course_name,
                total_records=total,
                present_count=present,
                absent_count=row.absent_count or 0,
                late_count=row.late_count or 0,
                leave_count=row.leave_count or 0,
                pending_count=row.pending_count or 0,
                attendance_rate=round(attendance_rate, 2),
            ))
        return summaries

    def get_absence_ranking(self, db: Session, course_id: str | None = None, top_n: int = 10) -> list[StudentAbsenceRank]:
        query = db.query(
            Attendance.student_id,
            Student.name.label('student_name'),
            Student.student_no.label('student_no'),
            func.sum(case((Attendance.status == AttendanceStatus.ABSENT, 1), else_=0)).label('absent_count'),
            func.sum(case((Attendance.status == AttendanceStatus.LATE, 1), else_=0)).label('late_count'),
            (func.sum(case((Attendance.status == AttendanceStatus.ABSENT, 1), else_=0)) +
             func.sum(case((Attendance.status == AttendanceStatus.LATE, 1), else_=0))).label('total_absent'),
        ).join(Student, Attendance.student_id == Student.id).group_by(Attendance.student_id, Student.name, Student.student_no)
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        results = query.order_by(desc('total_absent')).limit(top_n).all()
        ranks = []
        for idx, row in enumerate(results, start=1):
            ranks.append(StudentAbsenceRank(
                student_id=row.student_id,
                student_name=row.student_name,
                student_no=row.student_no,
                absent_count=row.absent_count or 0,
                late_count=row.late_count or 0,
                total_absent=row.total_absent or 0,
                rank=idx,
            ))
        return ranks

attendance_service = AttendanceService()
