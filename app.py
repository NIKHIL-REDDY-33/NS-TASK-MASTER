from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(500), nullable=False)
    completed=db.Column(db.Integer, default=0)
    created_date=db.Column(db.DateTime, default=datetime.utcnow)
    
    def _repr_(self):
        return '<Task %I>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'there was issue in adding the task'
    else:
        tasks = Todo.query.order_by(Todo.created_date).all()
        return render_template('index.html', tasks=tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete =  Todo.query.get_or_404(id)

    try :
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except :
        return 'there was a problem deleting the task'    

@app.route('/update/<int:id>' , methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content=request.form['content']

        try :
            db.session.commit()
            return redirect('/')
        except :
            return "there is an issue in updating the task"    
    else:
        return render_template('update.html',task=task)
if __name__=="__main__":
    app.run(debug=True)