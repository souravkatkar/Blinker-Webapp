from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.secret_key = 'HalaMadrid'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    score = db.Column(db.Integer)

db.create_all()
db.session.commit()

@app.route('/',methods=['GET'])
def index():
    
    return render_template('index.html')

@app.route('/game',methods=['POST','GET'])
def game():
    if request.method == 'POST':
        
        data = User.query.order_by(desc("score")).all()
        name = request.form['name']
        user = User.query.filter_by(name=name).first()
        
        if not user:
            db.session.add(User(name=name))
            db.session.commit()
        
        session['name'] = name
        
        return render_template('game.html',data = data)


    if request.method == 'GET':
        data = User.query.order_by(desc("score")).all()
        print(data)
        return render_template('game.html',data = data)

      

@app.route('/score',methods=['POST','GET'])
def score():
    if request.method == 'POST':
        score = request.form['score']
        name = session['name']
        print(name,score)
        user = User.query.filter_by(name=name).first()
        if user.score:
            if int(score) > user.score:
                user.score = score
                db.session.commit()
        else:
            user.score = score
            db.session.commit()
            
        return '',204
        
    


if __name__ == '__main__':
    app.run()
