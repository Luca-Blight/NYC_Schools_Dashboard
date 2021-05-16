import simplejson as json
from flask import Flask,request
from ..models import *
from ..db import *
from collections import defaultdict
from backend import DB_NAME,DB_HOST,DB_USER,DB_PASSWORD,DEBUG,TESTING
from flask.cli import FlaskGroup


#DBHOST - from_mapping
def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, 
                            DATABASE=DB_NAME,DEBUG=DEBUG,TESTING=TESTING)

    @app.route('/')
    def root_url():
        return 'Welcome to Schoolsy - always find the best school!'

    @app.route('/schools')
    def schools():
        conn = db.get_db()
        cursor = conn.cursor()
        
        schools = db.find_all(Schools, cursor)
        school_dict = [school.__dict__ for school in schools]
        
        scores = db.find_all(Scores, cursor)
        scores_dict = [score.__dict__ for score in scores]
        
        for score in scores_dict:
                score['id'] = score.pop('school_id')

        attendances = db.find_all(Attendance, cursor)
        attendance_dict = [attendance.__dict__ for attendance in attendances]
        for attendance in attendance_dict:
                attendance['id'] = attendance.pop('school_id')

        populations = db.find_all(Population, cursor)
        population_dict = [population.__dict__ for population in populations]
        for population in population_dict:
                population['id'] = population.pop('school_id')

        merged = defaultdict(dict)
        for l in (scores_dict,attendance_dict,population_dict,school_dict):
            for elem in l:
                merged[elem['id']].update(elem)

        return json.dumps(merged,default= str)


    @app.route('/schools/<id>')
    def attendance_id(id):
        conn = db.get_db()
        cursor = conn.cursor()

        school_obj = db.find(Schools, id, cursor)
        score_obj = db.find(Scores,id, cursor)
        population_obj = db.find(Population,id,cursor)
        attendance_obj = db.find(Attendance,id,cursor)

        school = school_obj.__dict__

        score =  score_obj.__dict__
        score['id'] = score.pop('school_id')

        population =  population_obj.__dict__
        population['id'] = int(population.pop('school_id'))

        attendance =  attendance_obj.__dict__
        attendance['id'] = attendance.pop('school_id')

        merged = defaultdict(dict)
        [merged[elem['id']].update(elem) for elem in (score,attendance,population,school)]
        return json.dumps(merged, default = str)

    return app


