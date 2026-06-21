from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel
from app.core.enums import AttendanceStatus

class AttendanceBase(BaseModel):
    course_id: UUID
    student_id: UUID
    date: date
    status: AttendanceStatus = AttendanceStatus.PENDING
    remark: str | None = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: AttendanceStatus | None = None
    remark: str | None = None

class AttendanceRead(AttendanceBase):
    id: UUID
    student_name: str | None = None
    course_name: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseAttendanceSummary(BaseModel):
    course_id: UUID
    course_name: str
    total_records: int
    present_count: int
    absent_count: int
    late_count: int
    leave_count: int
    pending_count: int
    attendance_rate: float

    class Config:
        from_attributes = True

class StudentAbsenceRank(BaseModel):
    student_id: UUID
    student_name: str
    student_no: str
    absent_count: int
    late_count: int
    total_absent: int
    rank: int

    class Config:
        from_attributes = True
