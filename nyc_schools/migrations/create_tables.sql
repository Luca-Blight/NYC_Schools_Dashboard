DROP TABLE IF EXISTS schools;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS student_population;


CREATE TABLE IF NOT EXISTS schools (
  id serial PRIMARY KEY,  
  nyc_id VARCHAR(255) UNIQUE,
  name VARCHAR(255),  
  address VARCHAR(255),
  zipcode VARCHAR(255),
  lat_lon VARCHAR(255),
  borough VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS scores (
  id serial PRIMARY KEY,
  school_id INTEGER,
  avg_score_sat_math FLOAT,
  avg_score_sat_reading_writing FLOAT,
  tot_sat_score FLOAT,
  graduation_rate FLOAT,
  ars_english FLOAT,
  ars_algebra FLOAT, 
  CONSTRAINT fk_school
  FOREIGN KEY(school_id) 
  REFERENCES schools(id)
);

CREATE TABLE IF NOT EXISTS attendance (
  id serial PRIMARY KEY, 
  school_id INTEGER,
  enrollment INTEGER,
  student_attendance VARCHAR(255),
  teacher_attendance VARCHAR(255),
  year TIMESTAMP,
  CONSTRAINT fk_school_id
  FOREIGN KEY(school_id) 
  REFERENCES schools(id)
);

CREATE TABLE IF NOT EXISTS student_population (
  id serial PRIMARY KEY,
  school_id INTEGER,
  english_language_learners FLOAT,
  percent_students_disabilities VARCHAR(255),
  economic_needs_idx VARCHAR(255),
  CONSTRAINT fk_school_id
  FOREIGN KEY(school_id) 
  REFERENCES schools(id)
);
