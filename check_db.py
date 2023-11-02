from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.String, primary_key=True)

if __name__ == '__main__':
    with app.app_context():
        users = Users.query.all()
        print("Users in the database:")
        for user in users:
            print(user.id)
