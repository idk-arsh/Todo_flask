from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ash.db'
db=SQLAlchemy(app)

class Register(db.Model):
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String(200),nullable=False)
    name=db.Column(db.String(200),nullable=False)

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


@app.route('/',methods=['GET','POST'])
def index333():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        existing_user=Register.query.filter_by(username=username).first()
        if existing_user is None:
            return redirect('/register/')
        else:
            password_check=Register.query.filter_by(password=password).first()
            if password_check is None:
                return "Ur Password is wrong"
            else:
                return redirect('/task/')

    else:    
        return render_template('signin.html')

@app.route('/register/',methods=['GET','POST'])
def index3():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        new_task=Register(name=name,username=username,password=password)
        existing_user=Register.query.filter_by(username=username).first()
        if existing_user is None:
            try:
                print("sucess")
                db.session.add(new_task)
                db.session.commit()
                return redirect('/task/')
            except:
                return "Something went Wrong"
        else:
            return "You are already registered"
    else:
        return render_template('register.html')

@app.route('/task/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']

        new_task=Task(content=task_content)

        # try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/task/')
        # except:
        #     return "Something went wrong. check again"
    else:

        tasks=Task.query.order_by(Task.date_created).all()
        return render_template('index.html',tasks=tasks)
    
@app.route('/task/delete/<id>')
def delete(id):
    task_to_be_deleted=Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_be_deleted)
        db.session.commit()
        return redirect('/task/')
    except:
        return "Something went wrong. check again"
    
@app.route('/task/update/<id>',methods=['POST','GET'])
def update(id):
    task=Task.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/task/')
        except:
            return "Something went wrong. check again"
    else:
        return render_template('update.html',task=task)



if __name__=='__main__':
    app.run(debug=True)