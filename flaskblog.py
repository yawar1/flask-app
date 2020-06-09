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
        mycur.execute("SELECT user,email FROM reg")
        result=mycur.fetchall()
        listnames=[]
        listemails=[]
        for i in result:
            listnames.append(i[0])
            listemails.append(i[1])
        if not(form.username.data in listnames):
            if not(form.email.data in listemails):
                mycur.execute(f"INSERT INTO reg(user,email,pass) VALUES('{form.username.data}','{form.email.data}','{form.password.data}')")
                db.commit()
                mycur.execute(f"CREATE TABLE table_{form.username.data}(blog LONGTEXT)")
                flash(f'Account created for {form.username.data}!','success')
                return redirect(url_for('home'))
            else:
                flash("Account with that email already exists!",'danger')
        else:
            flash("Username taken,try a diffrent one",'danger')
        return render_template('register.htm',
                            form=form,title='Register')
    else:
        return render_template('register.htm',
                            form=form,title='Register')
@app.route("/")
@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        mycur.execute(f"SELECT pass FROM reg WHERE user='{form.username.data}'")
        result=mycur.fetchone()
        if result:
            if form.password.data==result[0]:
                flash('Login Successful','success')
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful,please check your email and/or password','danger')
        else:
             flash('Account does not exist','danger')            
    return render_template('login.htm',title='Login',form=form)
     

if __name__=='__main__':
    app.run(debug=True)