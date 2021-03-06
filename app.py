from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'web'
app.config['MYSQL_PASSWORD'] = 'webPass'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'localhost' #for now
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Success"}'

@app.route("/delete") #delete Student
def delete():
  id2 = request.args.get('id')
  cur = mysql.connection.cursor()
  s = "delete from students where studentID = '%s'" % id2

  #sql = "delete from students where studentID = '%d'" % (id2)
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Delete Successful"}'

@app.route("/update") #update Student
def update():
  id3 = request.args.get('id')
  name3 = request.args.get('name')
  cur = mysql.connection.cursor()
  s = "update students set studentName = '%s' where studentID = '%s'" %(name3, id3)
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Update Successful"}'



#@app.route("/update") #update Student
#def update():
#  id3 = request.args.get('id')
 #   cur = mysql.connection.cursor()
  #  s = "update students set studentName = 'mary' WHERE studentid = '%s'" % id3
  #cur.execute(s)
  #mysql.connection.commit()  
  #return '{"Result":"Update not complete"}'

@app.route("/") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080
