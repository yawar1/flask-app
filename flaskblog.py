from flask import Flask,render_template,redirect,url_for,request,flash
from forms import RegistrationForm,LoginForm
import mysql.connector as sq
db=sq.connect(
    host="localhost",
    user="root",
    passwd="Nasamud@yahoopee5216",
    database="flask"
)
mycur=db.cursor()


app=Flask(__name__)
app.config['SECRET_KEY']='fwehdfaisuhfu'

posts=[
    {
        'author':'Corey Schafer',
        'title':'Blog post 1',
        'content':'First post content',
        'date_posted':'April 20,2018'
    },
    {
        'author':'Jane Doe',
        'title':'Blog post 2',
        'content':'Second post content',
        'date_posted':'April 21,2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.htm",title="home",posts=posts) 

@app.route('/about')
def about():
    
    return render_template('about.htm',
                          title="about")

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        mycur.execute(f"INSERT INTO reg(user,email,pass) VALUES('{form.username.data}','{form.email.data}','{form.password.data}')")
        db.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
        
    else:
        
        return render_template('register.htm',
                            form=form,title='Register')

@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        mycur.execute(f"SELECT pass FROM reg WHERE email='{form.email.data}'")
        if form.password.data==mycur.fetchone()[0]:
            flash('Login Successful','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful,please check your email and/or password','danger')
    return render_template('login.htm',title='Login',form=form)
     

if __name__=='__main__':
    app.run(debug=True)