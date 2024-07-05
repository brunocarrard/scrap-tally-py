from flask import Flask
from controllers.getters import Getters

app = Flask(__name__)

@app.route('/')
def hello_world():
        
    # To test the get_test_user_group function
    user_groups = Getters.get_users()

    print(user_groups)
    
    return "Hello World!"



if __name__ == '__main__':
    app.run(debug=True)