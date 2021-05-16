from .. import db

class Attendance:

    __table__ = 'attendance'
    columns = ['school_id', 'enrollment', 'student_attendance', 
                'teacher_attendance','year']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_id(self, school_id, cursor):
        attendance_query = f"""SELECT * FROM {self.__table__} WHERE school_id = %s"""
        cursor.execute(attendance_query, (school_id,))
        record = cursor.fetchone()
        return db.build_from_record(self, record)

   