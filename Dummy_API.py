from flask import Flask,jsonify,request
import json

app = Flask(__name__)
DATA_FILE='data.json'

with open(DATA_FILE, 'r') as f:
    employees = json.load(f)

#get all data
@app.route('/employees',methods=['GET'])
def get_employees():
    return jsonify(employees)

#get data by id
@app.route('/employees/<int:id>',methods=['GET'])
def get_employees_by_id(id):
    for i in employees:
        if i['id']==id:
            return jsonify(i)
    return jsonify({"message":"Employee not found"})

#post method (add data)
@app.route('/employees',methods=['POST'])
def add_employee():
    new_emp = request.get_json()
    employees.append(new_emp)

    with open(DATA_FILE, 'w') as f:
        json.dump(employees, f, indent=4)
    return jsonify({"message": "Employee added successfully!", "employee": new_emp}), 201

#put method (update)
@app.route('/employees/<int:id>',methods=['PUT'])
def update(id):
    data = request.get_json()
    for i in employees:
        if i["id"]==id:
            i.update(data)
            i["id"]=id
            with open(DATA_FILE,'w') as f:
                json.dump(employees,f,indent=4)
            return jsonify({"message":"Employee Updated Successfully!"})
    return jsonify({"message":"employee not found"})

#patch method (partial_update)
@app.route('/employees/<int:id>',methods=['PATCH'])
def partial_update(id):
    data = request.get_json()
    for i in employees:
        if i["id"]==id:
            for key,value in data.items():
                i[key]=value
                with open(DATA_FILE,'w') as f:
                    json.dump(employees,f,indent=4)
                    return jsonify({"message":"Employee update Successfully!"})
            return jsonify({"message":"User key not fount !"})
    return jsonify({"message":"employee not found !"})

#delete method 
@app.route('/employees/<int:id>',methods=['DELETE'])
def delete(id):
    for i in employees:
        if i["id"]==id:
            employees.remove(i)
            with open(DATA_FILE,'w') as f:
                json.dump(employees,f,indent=4)
                return jsonify({"message":"Employee deleted Successfully!"})
    return jsonify({"message":"employee not found !"})

if __name__=="__main__":
    app.run(debug=True)