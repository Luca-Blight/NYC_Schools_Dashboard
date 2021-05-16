from ..db import *
from ..models import *

class Population():

    __table__ = 'student_population'
    columns = ['school_id','english_language_learners','percent_students_disabilities','economic_needs_idx'] 


    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)
    @classmethod
    def find_by_id(self, school_id, cursor):
        population_query = f"""SELECT * FROM {self.__table__} WHERE school_id = %s"""
        cursor.execute(population_query, (school_id,))
        record = cursor.fetchone()
        return db.build_from_record(self, record)