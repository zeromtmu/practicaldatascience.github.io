import sqlite3, csv, pandas as pd, json, pymongo

def load_sql(conn, file_name):
  classes_file = open(file_name)
  conn.execute("CREATE TABLE classes(class TEXT, grade_1 INT, grade_2 INT, grade_3 INT);")
  rows = [(row['course'], row['midterm_1'], row['midterm_2'], row['midterm_3']) for row in csv.DictReader(classes_file)]
  classes_file.close()
  conn.executemany("INSERT INTO classes (class, grade_1, grade_2, grade_3) VALUES (?,?,?,?);", rows)
  conn.commit()
  print pd.read_sql("SELECT * FROM classes;", conn)

def pretty_print(d):
  return json.dumps(d, sort_keys=True, indent=2, separators=(',',': '))

def pretty_print_remove_id(s, _):
  pipeline = [{
    '$unwind': {
        "path": "$courses"
    }}, {
    '$project': {
      'courses': True,
      'name': True,
      '_id': False
    }
  }]
  return pretty_print(list(s.aggregate(pipeline)))