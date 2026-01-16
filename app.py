from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import    SQLAlchemy
from datetime import datetime

app_instance = Flask(__name__)
app_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
database = SQLAlchemy(app_instance)

# CREATING A MODEL
class Todo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    content = database.Column(database.String(200), nullable=False)
    completed = database.Column(database.Integer, default=0)
    date_created = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app_instance.route('/', methods=['POST', 'GET'])
def index ():
    # get form content form html form
    if request.method == 'POST':
        task_content = request.form['content'].strip()
        if not task_content:
            return redirect('/')
        new_task = Todo(content=task_content)
        try:
            database.session.add(new_task)
            database.session.commit()
            return redirect('/')
        except:
            return 'An error Occured when adding your task. Try again please'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app_instance.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        database.session.delete(task_to_delete)
        database.session.commit()
        return redirect('/')

    except:
        return 'An error occurred while deleting your task'
    
@app_instance.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            database.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while editing task. Try Again please'
    else:
        return render_template('update.html', title='Update', task=task)

if __name__ == '__main__':
    app_instance.run(debug=True)