# Import flask class, html render and the url decorator
from flask import Flask, render_template, url_for   
# Flask database configuration
from flask_sqlalchemy import SQLAlchemy


# Base class of flask where it will starts the web service
app = Flask(__name__)

# Set up database with flask alchemy and the sqlite engine 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     # 3 ///s with relative path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'  # 4 ////s with absolute path 
db = SQLAlchemy(app)


class Todo(db.Model):
    




# Url configurations
@app.route('/')

def index():
    # return 'hELLO worlD!!!'
    return render_template('index.html')


# Main
if __name__ == '__main__':
    app.run(debug=True)