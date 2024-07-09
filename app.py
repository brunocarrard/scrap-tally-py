from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)