from ..db.orm import *

class Scores():

    __table__ = 'scores'
    columns = ['id','school_id','avg_score_sat_math','avg_score_sat_reading_writing','tot_sat_score',
        'graduation_rate', 'ars_english','ars_algebra']

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
        record =  cursor.fetchone()
        return build_from_record(self, record)
