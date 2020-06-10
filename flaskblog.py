from flask import Flask,render_template,redirect,url_for,request,flash
from forms import RegistrationForm,LoginForm,PostForm
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


def home(author):
    mycur.execute("SELECT user FROM reg")
    result=mycur.fetchall()
    listnames=[]
    ListContent=[]
    for i in result:
        listnames.append(i[0])
    listnames.remove(author)
    for j in listnames:
        mycur.execute(f"SELECT blog from table_{j}")
        result1=mycur.fetchall()
        for k in result1:
            ListContent.append(k[0])
    return render_template("home.htm",title="home",posts=ListContent) 

@app.route('/about',methods=['GET','POST'])
def about():
    form=PostForm()
    if form.validate_on_submit():
        return redirect(url_for("login"))
    else:
        return render_template('about.htm',
                            title="about",form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        mycur.execute(f"SELECT * FROM reg WHERE user='{form.username.data}' ")
        result_pw=mycur.fetchone()
        mycur.execute(f"SELECT * FROM reg WHERE email='{form.email.data}' ")
        result_email=mycur.fetchone()
        if not(result_pw):
            if not(result_email):
                mycur.execute(f"INSERT INTO reg(user,email,pass) VALUES('{form.username.data}','{form.email.data}','{form.password.data}')")
                db.commit()
                mycur.execute(f"CREATE TABLE table_{form.username.data}(blog LONGTEXT)")
                flash(f'Account created for {form.username.data}!','success')
                return home(form.username.data)
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
                return home(form.username.data)
            else:
                flash('Login unsuccessful,please check your email and/or password','danger')
        else:
             flash('Account does not exist','danger')            
    return render_template('login.htm',title='Login',form=form)
     

if __name__=='__main__':
    app.run(debug=True)