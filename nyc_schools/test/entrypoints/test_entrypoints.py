import pytest
import psycopg2
from flask import json
from test_project.backend.src.db.orm import get_db, close_db, drop_records, save,drop_all_tables,find_all,find,find_by_school_id
from test_project.backend.src.models import *
from test_project.backend.settings import *


test_conn = psycopg2.connect(database="test_nyc_schools", host=DB_HOST,user=DB_USER,port=5432,password=DB_PASSWORD)
test_cursor = test_conn.cursor()

@pytest.fixture()
def seeded_tables():
    
    drop_all_tables(test_conn, test_cursor)

    orchard_school = save(Schools(id=1,nyc_id ='01M292',name='Orchard Collegiate Academy',address='220 HENRY STREET',zipcode='10002' ,lat_lon='40.713362,-73.986051',borough='MANHATTAN'), test_conn, test_cursor)
    university_school = save(Schools(id=2,nyc_id='01M448',name='University Neighborhood High School',address='200 MONROE STREET',zipcode='10002',lat_lon='40.712269,-73.984128',borough='MANHATTAN'),test_conn,test_cursor)

    orchard_scores = save(Scores(school_id=1, avg_score_sat_math=447.9,avg_score_sat_reading_writing=426.3,tot_sat_score=874.2,graduation_rate=65.80,ars_english=76.5,ars_algebra=67.1), test_conn, test_cursor)
    university_scores = save(Scores(school_id=2, avg_score_sat_math=495.2,avg_score_sat_reading_writing =456.8,tot_sat_score=952,graduation_rate=89.70,ars_english=73.1,ars_algebra=72.5), test_conn, test_cursor)


    orchard_attendance = save(Attendance(school_id=1, enrollment=140, student_attendance=0.867, teacher_attendance=0.973), test_conn, test_cursor)
    university_attendance = save(Attendance(school_id=2, enrollment=392, student_attendance=0.925, teacher_attendance=0.971), test_conn, test_cursor)

    orchard_population = save(Population(school_id=1, english_language_learners=0.143,percent_students_disabilities=0.271,economic_needs_idx=0.832), test_conn, test_cursor)
    university_population = save(Population(school_id=2, english_language_learners=0.089,percent_students_disabilities=0.148,economic_needs_idx=0.757), test_conn, test_cursor)

    yield seeded_tables

    drop_all_tables(test_conn, test_cursor)

#schools
def test_school_find(seeded_tables):
    school = find(Schools,1,test_cursor) 
    assert school.name == 'Orchard Collegiate Academy'

def test_school_find_all(seeded_tables):
    schools = find_all(Schools, test_cursor)
    assert [school.name for school in schools] == ['Orchard Collegiate Academy', 'University Neighborhood High School']

def test_school_latlon_length(seeded_tables):
    schools = find_all(Schools, test_cursor)
    lat_lon =  [school.lat_lon for school in schools][0]
    assert len(lat_lon.split(',')) == 2

def test_school_borough(seeded_tables):
    schools = find_all(Schools, test_cursor)
    boroughs = [school.borough for school in schools]
    assert boroughs[0] and boroughs[1] == 'MANHATTAN' or 'BROOKLYN' or 'QUEENS'

#scores
def test_scores_type(seeded_tables):
    score = find_by_school_id(Scores,1,test_cursor)
    assert type(score.avg_score_sat_math) == float
    assert type(score.avg_score_sat_reading_writing) == float


def test_scores_sat(seeded_tables):
    score = find_by_school_id(Scores,1, test_cursor)
    assert score.avg_score_sat_math + score.avg_score_sat_reading_writing == score.tot_sat_score

def test_scores_type(seeded_tables):
    score = find_by_school_id(Scores,1,test_cursor)
    assert type(score.tot_sat_score) == float
    assert type(score.graduation_rate) == float

def test_attendance_type(seeded_tables):
    school = find_by_school_id(Attendance,2, test_cursor)
    assert  type(school.enrollment) == int

def test_attendance_type_two(seeded_tables):
    school = find_by_school_id(Attendance,1, test_cursor)
    assert  type(school.student_attendance) == int

def test_student_population_type(seeded_tables):
    school = find_by_school_id(Population,1, test_cursor)
    assert  type(school.english_language_learners) == float

#adjust to int
def test_student_population_type(seeded_tables):
    school = find_by_school_id(Population,2, test_cursor)
    assert  type(school.economic_needs_idx) == str

# def test_table_ids(seeded_tables):
#     global test_cursor
#     sql_str = f"""SELECT * FROM schools JOIN scores ON scores.school_id = schools.id  
#                                                                       JOIN attendance ON attendance.school_id = schools.id  
#                                                                       JOIN student_population ON student_population.school_id = schools.id
#                                                                       WHERE schools.id = 1"""
#     results = test_cursor.execute(sql_str)
#     assert results == 1
 