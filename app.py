from math import e
from flask import Flask, request, jsonify
from controllers import scrap_tally
from controllers.getters import Getters
from controllers.scrap_tally import ScrapTally
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/users')
def get_users():
    user_groups = Getters.get_users()
    return jsonify(user_groups)

@app.route('/processes')
def get_processes():
    processes = Getters.get_processes()
    return processes

@app.route('/machines')
def get_machines():
    process = request.args.get('process', default='', type=str)
    machines = Getters.get_machines(process)
    return jsonify(machines)

@app.route('/defect-types') 
def get_defect_types(): 
    defect_types = Getters.get_defect_types() 
    return jsonify(defect_types)

@app.route('/defect-conditions') 
def get_defect_conditions():
    process = request.args.get('process', default='', type=str)
    defect_type = request.args.get('defect-type', default='', type=str) 
    defect_conditions = Getters.get_defect_conditions(process, defect_type) 
    return jsonify(defect_conditions)

@app.route('/parts') 
def get_parts():
    process = request.args.get('process', default='', type=str)
    parts = Getters.get_parts(process) 
    if len(parts) == 0:
        return jsonify({"error": "No part found for this process."}), 404
    return jsonify(parts)

@app.route('/part-type') 
def get_part_type():
    part = request.args.get('part', default='', type=str)
    part_type = Getters.get_part_type(part)
    return jsonify(part_type)

@app.route('/scrap-tally', methods=['POST']) 
def post_scrap_tally():
    payload = request.json
    defect = Getters.get_defect(payload.get('defectType'), payload.get('defectCondition'))
    ScrapTally.postScrap(payload, defect)
    return ('Scrap was inserted.')

@app.route('/scrap-tally') 
def get_scrap_tally():
    page = request.args.get('page', default=1, type=int)
    user_code = request.args.get('user_code', default=None, type=str)
    print(page, user_code)
    scrap_tally = Getters.get_scrap_table(page, user_code)
    return jsonify(scrap_tally)

@app.route('/scrap-tally', methods=['PATCH'])
def update_scrap_tally():
    payload = request.json
    defect = Getters.get_defect(payload.get('defectType'), payload.get('defectCondition'))
    last_upd_on = Getters.get_last_upd_on(payload.get('scrapTally'))
    ScrapTally.updateScrap(payload, defect, last_upd_on)
    return ('Scrap was updated.')

@app.route('/last-upd-on')
def get_last_upd_on():
    scrap_tally = request.args.get('scrapTally', default=None, type=int)
    last_upd_on = Getters.get_last_upd_on(scrap_tally)
    return jsonify(last_upd_on)

@app.route('/scrap-tally', methods=['DELETE'])
def delete_scrap_tally():
    payload = request.json
    last_upd_on = Getters.get_last_upd_on(payload.get('scrapTally'))
    ScrapTally.deleteScrap(payload, last_upd_on)
    return ('Scrap was deleted.')

if __name__ == '__main__':
    app.run(debug=True)