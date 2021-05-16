from .. import db
# import nyc_schools.backend.api.src.models as models

class Schools():

    __table__ = 'schools'
    columns = ['id','nyc_id', 'name','address',
        'zipcode','lat_lon','borough']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    @classmethod
    def find_by_id(self, school_id, cursor):
        attendance_query = f"""SELECT * FROM {self.__table__} WHERE nyc_id = %s"""
        cursor.execute(attendance_query, (school_id,))
        record =  cursor.fetchone()
        return db.build_from_record(self, record)

    @classmethod
    def reference_by_id(self, school_id, cursor):
        school_query = f"""SELECT * FROM {self.__table__} WHERE nyc_id = %s"""
        cursor.execute(school_query, (school_id,))
        record = cursor.fetchone()
        if record:
            return record[0]
        else:
            pass