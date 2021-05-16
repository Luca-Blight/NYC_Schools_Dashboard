import pytest
import psycopg2
import os
from flask import json
from nyc_schools.backend.src.db import save,drop_all_tables,find_all
from nyc_schools.backend.src.models import Schools,Attendance,Population,Scores


test_conn = psycopg2.connect(database = 'nyc_schools_test', user = 'postgres', password = 'postgres')
test_cursor = test_conn.cursor()


@pytest.fixture()
def build_tables():

    drop_all_tables(test_conn, test_cursor)

    school_record_one = Schools(id = 1, nyc_id = 1, name = 'The_best_high_school', address = 'The_best_location', zipcode = '77777', lat_lon = '43,43', borough = 'Manhattan')
    school_record_two = Schools(id = 2, nyc_id = 2, name = 'The_worst_high_school', address = 'The_worst_location', zipcode = '66666', lat_lon = '34,34', borough = 'Bronx')  

    save(school_record_one, test_conn, test_cursor)
    save(school_record_two, test_conn, test_cursor)

    # attendance_record_one = Attendance(school_id=1,enrollment=200,student_attendance=95,teacher_attendance=100)
    # attendance_record_two = Attendance(school_id=2,enrollment=1000,student_attendance=66,teacher_attendance=86)
    
    # save(attendance_record_one, test_conn, test_cursor)
    # save(attendance_record_two, test_conn, test_cursor)

    # population_record_one = Population(school_id=1,english_language_learners=60,percent_students_disabilities=10,economic_needs_idx=25)
    # population_record_two = Population(school_id=2,english_language_learners=20,percent_students_disabilities=50,economic_needs_idx=75)

    # save(population_record_one, test_conn, test_cursor)
    # save(population_record_two, test_conn, test_cursor)
    
    # scores_record_one = Scores(id=1,school_id=1,avg_score_sat_math=800,avg_score_sat_reading_writing=800,tot_sat_score=1600,graduation_rate=100, ars_english=99,ars_algebra=99)
    # scores_record_two = Scores(id=2,school_id=2,avg_score_sat_math=400,avg_score_sat_reading_writing=421,tot_sat_score=821,graduation_rate=45, ars_english=33,ars_algebra=44)
    
    # save(scores_record_one, test_conn, test_cursor)
    # save(scores_record_two, test_conn, test_cursor)

    yield

    drop_all_tables(test_conn, test_cursor)


def test_find_all(build_tables):
     school_names = find_all(Schools, test_cursor)
     assert [school.name for school in school_names] == ['The_best_high_school', 'The_worst_high_school']