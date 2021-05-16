from ..models import *
from ..db import *
from .client import school_loc_details,attn_pop_details
from .scores_data import scores_details
import json


class ParentBuilder:

    def school_run(self,school_details=school_loc_details,conn=orm.conn_dev):
        cursor = conn.cursor()
        schools = SchoolBuilder().run(school_details, conn, cursor)
        return schools

    def attn_run(self,school_details=attn_pop_details,conn=orm.conn_dev):
        cursor = conn.cursor()
        attendance = AttendanceBuilder().run(school_details, conn, cursor)
        return attendance

    def pop_run(self,school_details=attn_pop_details,conn=orm.conn_dev):
        cursor = conn.cursor()
        population = PopulationBuilder().run(school_details, conn, cursor)
        return population

    def scores_run(self,school_details=scores_details,conn=orm.conn_dev):
        cursor = conn.cursor()
        scores = ScoresBuilder().run(school_details, conn, cursor)
        return scores
        
class SchoolBuilder:
 
    attributes = ['nyc_id', 'name','address',
        'zipcode','lat_lon','borough']

    def select_attributes(self, school_loc_data):
          schools = []
          for data in school_loc_data:
            if data.get('location_category_description') == 'High school':
              nyc_id,name,address = data.get('ats_system_code','').strip(),data.get('location_name',''),data.get('primary_address_line_1','').strip()
              zipcode = json.loads(data.get('location_1','')['human_address'])['zip']
              borough = json.loads(data.get('location_1','')['human_address'])['city']
              lat_lon = data.get('location_1','')['latitude'] + ',' +  data.get('location_1','')['longitude']
              schools.append(dict(zip(self.attributes,[nyc_id, name, address, zipcode,lat_lon,borough])))
          return schools
    
    def run(self, school_data, conn, cursor):
        selected_attrs = self.select_attributes(school_data)
        schools_written = []
        for selected_attr in selected_attrs:
            nyc_id = selected_attr['nyc_id'] 
            schools = Schools.find_by_id(nyc_id, cursor)
            if schools:
                schools.exists = True
            else:
                schools = orm.save(Schools(**selected_attr), conn, cursor)
                schools.exists = False
                schools_written.append(schools)
        return schools_written

class PopulationBuilder:

    population_attributes = ['school_id','english_language_learners','percent_students_disabilities','economic_needs_idx'] 
                
    def select_attributes(self, attn_pop_data, cursor):
        schools = []
        for data in attn_pop_data:
            dbn=data.get('dbn','')
            school_reference_id = Schools.reference_by_id(dbn,cursor)
            school_id = school_reference_id
            if school_reference_id:
                english_language_learners=data.get('percent_english_language',' ')
                percent_students_disabilities=data.get('percent_students_with','')
                economic_needs_idx=data.get('economic_need_index','')
                schools.append(dict(zip(self.population_attributes,[school_id, english_language_learners, percent_students_disabilities, economic_needs_idx])))
        return schools


    def run(self, school_data, conn, cursor):
        selected_attrs = self.select_attributes(school_data,cursor)
        schools_written = []
        for selected_attr in selected_attrs:
            school_id = selected_attr['school_id'] 
            population = Population.find_by_id(school_id, cursor)
            if population:
                population.exists = True
            else:
                population = orm.save(Population(**selected_attr), conn, cursor)
                population.exists = False
                schools_written.append(population)
        return schools_written

class AttendanceBuilder:

    attendance_attributes = ['school_id','enrollment', 'student_attendance', 
                'teacher_attendance','year'] 
                
    def select_attributes(self, attn_pop_data,cursor):
        schools = []
        for data in attn_pop_data:
            dbn=data.get('dbn','')
            school_reference_id = Schools.reference_by_id(dbn,cursor)
            if school_reference_id:
                school_id = school_reference_id
                enrollment=data.get('enrollment',' ')
                student_attendance=data.get('student_attendance_rate','')
                teacher_attendance=data.get('teacher_attendance_rate','')
                schools.append(dict(zip(self.attendance_attributes,[school_id, enrollment, student_attendance, teacher_attendance])))
        return schools

    def run(self, school_data, conn, cursor):
        selected_attrs = self.select_attributes(school_data,cursor)
        schools_written = []
        for selected_attr in selected_attrs:
            school_id = selected_attr['school_id'] 
            attendance = Attendance.find_by_id(school_id, cursor)
            if attendance:
                attendance.exists = True
            else:
                attendance = orm.save(Attendance(**selected_attr), conn, cursor)
                attendance.exists = False
                schools_written.append(attendance)
        return schools_written


class ScoresBuilder:

    scores_attributes = ['school_id','avg_score_sat_math', 'avg_score_sat_reading_writing', 'tot_sat_score',
                'graduation_rate','ars_english','ars_algebra'] 
    
    def select_attributes(self, score_data, cursor):
        schools = []
        for data in score_data:
            dbn=data.get('DBN','')
            school_reference_id = Schools.reference_by_id(dbn,cursor)
            if school_reference_id:
                school_id = school_reference_id
                avg_score_sat_math=data.get(' Average Score SAT Math','')
                avg_score_sat_reading_writing=data.get('Average Score SAT Reading and Writing','')
                tot_sat_score = round(avg_score_sat_math+avg_score_sat_reading_writing,2)
                graduation_rate=data.get('4-Year Graduation Rate','')               
                ars_english=data.get('Average Regents Score - English ','')
                ars_algebra=data.get(' Average Regents Score - Algebra I ','')
                schools.append(dict(zip(self.scores_attributes,[school_id,avg_score_sat_math, avg_score_sat_reading_writing,tot_sat_score,graduation_rate,ars_english,ars_algebra])))
        return schools

    def run(self, school_data, conn, cursor):
        selected_attrs = self.select_attributes(school_data,cursor)
        schools_written = []
        for selected_attr in selected_attrs:
            school_id = selected_attr['school_id'] 
            scores = Scores.find_by_id(school_id, cursor)
            if scores:
                scores.exists = True
            else:
                scores = orm.save(Scores(**selected_attr), conn, cursor)
                scores.exists = False
                schools_written.append(scores)
        return schools_written