from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import warnings
import urllib3

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.String, primary_key=True)

class UserActivity(db.Model):
    __tablename__ = 'UserActivity'

    id = db.Column(db.Integer, primary_key=True)  # primary key
    user_id = db.Column(db.String, db.ForeignKey('Users.id'))
    online_time = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<UserActivity {self.id}>'

def get_user_info(user_id):
    print(f"Fetching info for user {user_id}")
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?userId={user_id}"
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"User data: {user_data}")
        for user in user_data.get('data', []):
            if user['userId'] == user_id:
                result = {
                    'userId': user['userId'],
                    'nickname': user['nickname'],
                    'firstSeen': user['registrationDate']
                }
                print(f"Returning: {result}")
                return result
    print("User not found or request failed")
    return None

@app.route('/api/users/list', methods=['GET'])
def get_users_list():
    user_ids = [user.id for user in Users.query.all()]
    print("User IDs from DB:", user_ids)
    result = []
    for user_id in user_ids:
        print("Getting info for user:", user_id)
        user_info = get_user_info(user_id)
        print("User info:", user_info)
        if user_info:
            result.append({
                'username': user_info['nickname'],
                'userId': user_info['userId'],
                'firstSeen': user_info['firstSeen']
            })

    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
