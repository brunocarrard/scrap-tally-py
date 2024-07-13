from flask import Flask, request
from controllers.getters import Getters
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/users')
def get_users():
    user_groups = Getters.get_users()
    return user_groups

@app.route('/processes')
def get_processes():
    processes = Getters.get_processes()
    return processes

@app.route('/machines')
def get_machines():
    process = request.args.get('process', default='', type=str)
    machines = Getters.get_machines(process)
    return machines

@app.route('/defect-types') 
def get_defect_types(): 
    defect_types = Getters.get_defect_types() 
    return defect_types 

@app.route('/defect-conditions') 
def get_defect_conditions(): 
    defect_type = request.args.get('defect-type', default='', type=str) 
    defect_conditions = Getters.get_defect_conditions(defect_type) 
    return defect_conditions

if __name__ == '__main__':
    app.run(debug=True)