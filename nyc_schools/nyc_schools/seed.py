import psycopg2
from src.models import *
import pandas as pd
from sodapy import Socrata
from orm import *
from autopep8 import *

app_token = 'XNKZJVsscuBPRteOXyyM6G3yc'

conn = psycopg2.connect(database = 'project_one', user = 'postgres', password = 'postgres')
cursor = conn.cursor()
client = Socrata(domain = "data.cityofnewyork.us", app_token = app_token)
data = client.get("ewhs-k7um", content_type = "json")


#Results
school_one_dummy = save(School(nyc_id='01M292', name='Orchard Collegiate Academy', zipcode=10009,lat_lon=['40.71','-73.988'],neighborhood='East Village'), conn, cursor)

school_two_dummy = save(School(nyc_id='01M509', name='Marta Valle High School', zipcode=10009,lat_lon=['40.72004', '-73.986'], neighborhood = 'East Village'), conn, cursor)

school_three_dummy = save(School(nyc_id='01M450', name='East Side Community School', zipcode=10002,lat_lon=['40.729389','-73.982498'], neighborhood = 'Lower East Side'), conn, cursor)

school_four_dummy = save(School(nyc_id='02M374', name='Gramercy Arts High School', zipcode=10003,lat_lon=['40.735361','-73.98'], neighborhood = 'Gramercy'), conn, cursor)


#Scores
results_one_dummy = save(Scores(school_id=school_one_dummy.id, avg_score_sat_math=448 ,avg_score_sat_reading_writing=426 ,
        graduation_rate=66 ,ars_english=77 , ars_algebra=67), conn, cursor)

results_two_dummy = save(Scores(school_id=school_two_dummy.id, avg_score_sat_math=445,avg_score_sat_reading_writing=475,
        graduation_rate=74,ars_english=67,ars_algebra=59), conn, cursor)

results_three_dummy = save(Scores(school_id=school_three_dummy.id, avg_score_sat_math=497 ,avg_score_sat_reading_writing=521 ,
        graduation_rate=92 ,ars_english=80 , ars_algebra=75), conn, cursor)

results_four_dummy = save(Scores(school_id=school_four_dummy.id,avg_score_sat_math=462,avg_score_sat_reading_writing=481,
        graduation_rate=81,ars_english=75,ars_algebra=68), conn, cursor)
# first_dummy = save(Attendance(school_id=school_one_dummy.id, enrollment = 50, student_attendance = 75, 
#                 chronic_absence = 40.5, year = 2017),conn,cursor)

# second_dummy = save(Attendance(school_id=school_two_dummy.id, enrollment = 50, student_attendance = 75, 
#                 chronic_absence = 40.5, year = 2017),conn,cursor)



#         price = 3, rating = 4, likes = 15, menu_url = 'cafemogador.com')
# save(famiglia, conn, cursor)
# save(mogador, conn, cursor)

# pizza = Category(name = 'Pizza')
# italian = Category(name = 'Italian')

# save(pizza, conn, cursor)
# save(italian, conn, cursor)




#  __table__ = 'attendance'
#     columns = ['school_id', 'enrollment', 'student_attendance', 
#                 'chronic_absence','year']
#     pass


