from flask import Flask
from controllers.getters import Getters
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    # To test the get_test_user_group function
    user_groups = Getters.get_users()
    return user_groups

if __name__ == '__main__':
    app.run(debug=True)