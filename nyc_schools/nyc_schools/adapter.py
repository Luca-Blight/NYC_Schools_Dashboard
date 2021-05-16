import src.models as models
import src.db as db
import src.adapters as adapters
import src.psycopg2

class Attendance_PopBuilder:
    #attendance: DBN(school_id),student_attendance_rate(student_attendance),teacher_attendance_rate(teacher_attendance),year(16/17)
    attendance_attributes = ['school_id', 'enrollment', 'student_attendance', 
                'teacher_attendance','year'] 
    #student_population: DBN(school_id),enrollment(enrollment),Percent English Language Learners(percent_english_language_learners),
    #Percent of students chronically absent(percent_students_disabilities) FLOAT,
    #Economic Need Index(economics_needs_idx) FLOAT
    population_attributes = ['school_id', 'english_language_learners',
    'percent_students_disabilities','economics_needs_idx']
#dbn = 'school_id'
    def select_attributes(self, data_set):
        schools = []
        for d in data_set:
          school_id, enrollment, student_attendance, teacher_attendance = d.get('dbn',''),d.get('enrollment',''),d.get('student_attendance_rate',''),d.get('teacher_attendance_rate','')
          schools.append(dict(zip(self.attendance_attributes,[school_id, enrollment, student_attendance, teacher_attendance])))
        return schools
    
    # def run_attendance(self, data_set, conn, cursor):
    #     selected = self.select_attributes(venue_details)
    #     school_id = selected['school_id']
    #     venue = models.Attendance.find_by_id(foursquare_id, cursor)
    #     if venue:
    #         venue.exists = True
    #         return venue
    #     else:
    #         venue = db.save(models.Venue(**selected), conn, cursor)
    #         venue.exists = False
    #         return venue         
        # if menu_url:
        #     menu_url = menu_url.get('url', '').split('?')[0]
        # foursquare_id, name, price, rating = venue_details['id'], venue_details['name'], venue_details.get('price', {}).get('tier', None), venue_details.get('rating', None)
        # likes = venue_details.get('likes', {}).get('count', None)
        # return dict(zip(self.attributes, [foursquare_id, name, price, rating, likes, menu_url]))

derived_columns = Attendance_PopBuilder().select_attributes(attn_pop_details)
# attn_pop_missingobjects = Attendance_PopBuilder(attn_pop_details):