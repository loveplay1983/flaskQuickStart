# Import flask class, html render and the url decorator
from flask import Flask, render_template, url_for, request, redirect
# Flask database configuration
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta



# Base class of flask where it will starts the web service
app = Flask(__name__)

# Set up database with flask alchemy and the sqlite engine 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     # 3 ///s with relative path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'  # 4 ////s with absolute path 
db = SQLAlchemy(app)

# set up timer for cache clean
# https://www.cnblogs.com/zhenggaoxiong/p/9465440.html
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# app.send_file_max_age_default = timedelta(seconds=1)


class Todo(db.Model):
    """ 
    - Inherited from SQLAlchemy Base class 
    - Base class for SQLAlchemy declarative base model.
    - from flask_sqlalchemy.model import Model  flask_sqlalchemy.__init__.py
    - class SQLAlchemy(object):
    - ...
    -  This class also provides access to all the SQLAlchemy functions and classes
    from the :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` modules.  So you can
    declare models like this::

        class User(db.Model):
            username = db.Column(db.String(80), unique=True)
            pw_hash = db.Column(db.String(80))
    """  
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task   %r>' % self.id


# Url configurations
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['post_content_name']
        new_task = Todo(content=task_content)

        try:
            # add data to the db through db session
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')   # redirect the page back to the root path
        except:
            return 'Error occurred while adding the new task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # first tasks is the index.html jinjia2 variable, the second tasks is the tasks variable in this func
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There is a problem to deleteing that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an problem to update the data'
    else:
        # task=task  (first task is the template update.html task var, the second task is the task var in this func)
        return render_template('update.html', task=task)




# Main
if __name__ == '__main__':
    app.run(debug=True)