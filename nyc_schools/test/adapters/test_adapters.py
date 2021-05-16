import psycopg2
import pytest
from test_project.backend.src.adapters import *
from test_project.backend.src.adapters.builder import *
from test_project.backend.src.db import *
# from test_project.backend import TEST_DB_NAME,TEST_DB_HOST,TEST_DB_PASSWORD,TEST_DB_USER

loc_details = school_loc_details[:3]
pop_details = attn_pop_details[:3] 
# scores_details = scores_details[:3]

test_conn = psycopg2.connect(database="test_nyc_schools", host="localhost",user="postgres",password="postgres",port=5432)
test_cursor = test_conn.cursor()

@pytest.fixture()
def conn():
    drop_all_tables(test_conn, test_cursor)
    yield test_conn
    drop_all_tables(test_conn, test_cursor)

def test_school_etl(conn):
    school_objs = SchoolBuilder().run(school_data=loc_details,conn=test_conn,cursor=test_cursor)
    school_obj = school_objs[0]
    assert school_obj.nyc_id == '01M292'
    assert school_obj.name == 'Orchard Collegiate Academy' 
    assert school_obj.address == '220 HENRY STREET'
    assert school_obj.zipcode == '10002' 
    assert school_obj.lat_lon == '40.713362,-73.986051'
    assert school_obj.borough == 'MANHATTAN'

def test_population_etl(conn):
    school_objs = PopulationBuilder().run(school_data=pop_details,conn=test_conn,cursor=test_cursor)
    school_obj = school_objs[0]
    assert school_obj.english_language_learners == 1
    assert school_obj.percent_students_disabilities == 0.143
    assert school_obj.economic_needs_idx == '0.271'


#resolve issue
def test_attendance_etl(conn):
    attendance_objs = AttendanceBuilder().run(school_data=pop_details,conn=test_conn,cursor=test_cursor)
    attendance_obj = attendance_objs[0]
    assert attendance_obj.enrollment == 140
    assert attendance_obj.student_attendance == '0.867'
    assert attendance_obj.teacher_attendance == '0.973'

# {'school_id': 1, 'enrollment': 1, 'student_attendance': 140, 'teacher_attendance': '0.867', 'year': '0.973', 'exists': False}

# def test_scores_etl(conn):
#     scores_objs = ScoresBuilder().run(school_data=scores_details,conn=test_conn,cursor=test_cursor)
#     score_obj = scores_objs[0]
#     assert score_obj.avg_score_sat_math == 447.9
#     assert score_obj.avg_score_sat_reading_writing == 426.3
#     assert score_obj.tot_sat_score == 874.2
#     assert score_obj.graduation_rate == 65.8
#     assert score_obj.ars_english == 76.5
#     assert score_obj.ars_algebra == 67.1
