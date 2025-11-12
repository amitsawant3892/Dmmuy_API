from flask import Flask,jsonify,Response,request
import json
import xmltodict
import sqlite3
from collections import OrderedDict
from pydantic import BaseModel, Field, ValidationError,EmailStr
from typing import Optional, Literal, List


app = Flask(__name__)

#create database
def get_db():
    conn = sqlite3.connect("emp.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

#create tables
def create_table():
    conn = get_db()


    conn.execute('''CREATE TABLE IF NOT EXISTS employees (
                 emp_id INTEGER PRIMARY KEY,
                 emp_name TEXT NOT NULL,
                 salary REAL NOT NULL,
                 email TEXT UNIQUE NOT NULL )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS project (
                 project_id INTEGER PRIMARY KEY,
                 project_name TEXT UNIQUE NOT NULL
                 )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS employees_project (
                 emp_id INTEGER,
                 project_id INTEGER,
                 status VARCHAR(20),
                 PRIMARY KEY (emp_id, project_id),
                 FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                 ON DELETE CASCADE
                 ON UPDATE CASCADE,
                 FOREIGN KEY (project_id) REFERENCES project(project_id)
                 ON DELETE CASCADE
                 ON UPDATE CASCADE)''')
    conn.commit()
    conn.close()

#call create table function
create_table()


#create class for data validation
class Project(BaseModel):
    project_id:int
    project_name:str
    status:Literal['Completed','Ongoing','Pending']

class Employee(BaseModel):
    emp_id:int
    emp_name:str
    salary:float
    email:EmailStr
    project:list[Project]



#get all data by field name
@app.route('/employees',methods=['GET'])
def get_employees():

    name = request.args.get('emp_name')
    salary = request.args.get('salary')
    id = request.args.get('emp_id')
    email = request.args.get('email')
    conn=get_db()
    cursor=conn.cursor()

    emp = []

    #check the field
    if name:
        cursor.execute("Select * from employees where emp_name=?",(name,))
        row = cursor.fetchall()

    elif salary:
        cursor.execute("Select * from employees where salary = ?",(salary,))
        row = cursor.fetchall()

    elif id:
        cursor.execute("Select * from employees where emp_id=?",(id,))
        row = cursor.fetchall()
    
    elif email:
        cursor.execute("Select * from employees where email=?",(email,))
        row = cursor.fetchall()
    else:
        row = []


    #select all project using emp id
    for i in row:
        cursor.execute("select project_id, project_name,status from project join employees_project using(project_id) join employees using(emp_id) where emp_id=?",(i[0],))
        project= cursor.fetchall()
        projects = [{"project_id":c[0],"project_name":c[1],"status":c[2]} for c in project]
        

        # order data by sequence 
        emp.append(OrderedDict([
        ("emp_id", i[0]),
        ("emp_name", i[1]),
        ("salary",i[2]),
        ("email", i[3]),
        ("Projects",projects)]))
    conn.close()

    #getting data in json format
    return Response(
        json.dumps(emp, indent=4), 
        mimetype='application/json'
    )


#get all data 
@app.route('/all',methods=['GET'])
def get_all_employees():
    conn = get_db()
    cursor = conn.cursor()
    
    #select all data from collage table 
    cursor.execute("Select * from employees")
    row = cursor.fetchall()
    

    emp = []

    #select all project using emp id
    for i in row:
        cursor.execute("select project_id, project_name,status from project join employees_project using(project_id) join employees using(emp_id) where emp_id=?",(i[0],))
        project= cursor.fetchall()
        projects = [{"project_id":c[0],"project_name":c[1],"status":c[2]} for c in project]
        

        # order data by sequence 
        emp.append(OrderedDict([
        ("emp_id", i[0]),
        ("emp_name", i[1]),
        ("salary",i[2]),
        ("email", i[3]),
        ("projects",projects)]))
    conn.close()

    #getting data in json format
    return Response(
        json.dumps(emp, indent=4), 
        mimetype='application/json'
    )

#post method (add data)
@app.route('/employees',methods=['POST'])
def add_employee():

    #checks the file type and import in json
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/xml':
        data = xmltodict.parse(request.get_data())
    else:
        return jsonify({"message":"data format error! "})
    
    conn = get_db()
    cursor = conn.cursor()
 
    try:
        # check data is list or not
        records = data if isinstance(data,list) else [data]

        # get the data in rescods
        for item in records:
            #unpack with class
            new_data = Employee(**item)

            cursor.execute("Insert into employees(emp_id,emp_name,salary,email) values(?,?,?,?)",
                        (new_data.emp_id,
                         new_data.emp_name,
                         new_data.salary,
                         new_data.email
                        ))
        #insert values in course table
        for c in new_data.project:
             
            #Check if project already exists
             cursor.execute("SELECT project_id FROM project WHERE project_id = ?", (c.project_id,))
             existing_project = cursor.fetchone()

             if not existing_project:
                 cursor.execute("Insert into project(project_id, project_name) values(?,?)",
                                (c.project_id,
                                 c.project_name))
             
             cursor.execute("Insert into employees_project(emp_id,project_id,status) values(?,?,?)",
                            (
                             new_data.emp_id,
                             c.project_id,
                             c.status))
   
        conn.commit()
        conn.close()
        return jsonify({"Message":"employee Added !"})
    
    except ValidationError as e:
        return jsonify({"message": e.errors()[0]['msg']})
    
#put method (update)
@app.route('/employees/<int:id>',methods=['PUT'])
def update(id):

    class Project_Update(BaseModel):
        project_id:int
        project_name:str
        status:Literal['Completed','Ongoing','Pending']

    class Employee_Update(BaseModel):
        emp_name:str
        salary:float
        email:EmailStr
        project:list[Project_Update]

    #checks the file type and import in json
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/xml':
        data = xmltodict.parse(request.get_data())
    else:
        return jsonify({"message":"data format error! "})
    
    conn = get_db()
    cursor = conn.cursor()

    try:
        # check data is list or not
        records = data if isinstance(data,list) else [data]

        # get the data in records
        for item in records:
            #unpack with class
            new_data = Employee_Update(**item)
            cursor.execute("Select emp_id from employees where emp_id=?",(id,))
            exist_emp = cursor.fetchone()
            
            if not exist_emp:
                return jsonify({"message":"Employee not fount !"})
            
            cursor.execute("Update employees SET emp_name=?,salary=?,email=? where emp_id=?",
                        (
                         new_data.emp_name,
                         new_data.salary,
                         new_data.email,
                         id
                        ))
        #insert values in course table
        for c in new_data.project:
             
            #Check if project already exists
             cursor.execute("SELECT project_id FROM project WHERE project_id = ?", (c.project_id,))
             existing_project = cursor.fetchone()

             if not existing_project:
                 cursor.execute("Insert into project(project_id, project_name) values(?,?)",
                                (c.project_id,
                                 c.project_name))
                 
             cursor.execute("SELECT project_id FROM employees_project WHERE project_id = ? and emp_id=?", (c.project_id,id))
             assign_project = cursor.fetchone()

             if not assign_project:
                 cursor.execute("Update employees_project SET emp_id=?, project_id=?,status=?",
                            (
                             id,
                             c.project_id,
                             c.status))
   

             cursor.execute("Update employees_project SET status=? WHERE project_id = ? and emp_id=?",
                            (c.status,
                             c.project_id,
                             id))
   
        conn.commit()
        conn.close()
        return jsonify({"Message":"employee Updated !"})
    
    except ValidationError as e:
        return (e.errors())#jsonify({"message": e.errors()[0]['msg']})

    

#patch method (partial_update)
@app.route('/employees/<int:id>',methods=['PATCH'])
def partial_update(id):

    #checks the file type and import in json
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'application/xml':
        data = xmltodict.parse(request.get_data())
    else:
        return jsonify({"message":"data format error! "})
    
    conn = get_db()
    cursor = conn.cursor()

    class partial_update(BaseModel):
        emp_name:Optional[str]=None
        salary:Optional[float]=None
        email:Optional[EmailStr]=None
        project:Optional[list[Project]]=None
    
    try:
        update_data = partial_update(**data).model_dump(exclude_unset=True)

        for key, value in update_data.items():

            if key == "project":
                     for c in update_data["project"]:
                         
                         #Check if project already exists
                         cursor.execute("SELECT project_id FROM project WHERE project_id = ?", (c["project_id"],))
                         existing_project = cursor.fetchone()
                         
                         if not existing_project:
                            cursor.execute("Insert into project(project_id, project_name) values(?,?)",
                                            (c["project_id"],
                                            c["project_name"]))
                        
                         cursor.execute("SELECT project_id FROM employees_project WHERE project_id = ? and emp_id=?", (c["project_id"],id))
                         assign_project = cursor.fetchone()
                         
                         if not assign_project:
                             cursor.execute("Update employees_project SET emp_id=?, project_id=?,status=?",
                                             ( id,
                                             c["project_id"],
                                             c["status"]))
            

                         cursor.execute("Update employees_project SET status=? WHERE project_id = ? and emp_id=?",
                                             ( 
                                             c["status"],
                                             c["project_id"],
                                             id
                                             ))
            

            
                         conn.commit()
                         conn.close()
                         return jsonify({"Message":"employee Updated !"})
             
             
             
            query = f"UPDATE employees SET {key} = ? WHERE emp_id = ?"
            cursor.execute(query, (value, id))

    except ValidationError as e:
        return (e.errors())#jsonify({"message": e.errors()[0]['msg']})

    
            
#delete method 
@app.route('/employees/<int:id>',methods=['DELETE'])
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees WHERE emp_id=?", (id,))
    emp = cursor.fetchone()

    if not emp:
        conn.close()
        return jsonify({"message": "Employee not found!"})
    
    

    
    # Delete employee 
    cursor.execute("DELETE FROM employees WHERE emp_id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Employee deleted successfully!"}), 200

if __name__=="__main__":
    app.run(debug=True) 
