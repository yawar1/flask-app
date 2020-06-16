from flask import Flask,render_template,redirect,url_for,request,flash,session
from forms import RegistrationForm,LoginForm,PostForm
import mysql.connector as sq
import re
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

@app.route('/home')
def home():
    if not(session.get('user')):
        return redirect(url_for('login'))
    author=session.get('user')
    mycur.execute(f""" SELECT title,content,author,date_ FROM posts WHERE author <> '{author}' ORDER BY date_ DESC """)
    posts=mycur.fetchall()
    return render_template("home.htm",title="home",posts=posts) 

@app.route('/write',methods=['GET','POST'])
def write():
    if not(session.get('user')):
        return redirect(url_for('login'))
    form=PostForm()
    if form.validate_on_submit():
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        mycur.execute(f"""INSERT INTO posts(title,content,author,date_)
        VALUES("{form.title.data}","{form.Text.data}","{session.get('user')}",'{now}')""")
        db.commit()
        return home()
    else:
        return render_template('write.htm',
                            title="write",form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    if session.get('user'):
        return home()
    form=RegistrationForm()
    if form.validate_on_submit():
        flag=True
        p=re.compile('\W')
        result_reg=p.findall(form.username.data)
        for i in form.email.data:
            if ord(i)==34:
                flag=False
        if not(result_reg):
            mycur.execute(f'SELECT * FROM reg WHERE user="{form.username.data}" ')
            result_pw=mycur.fetchone()
            mycur.execute(f'SELECT * FROM reg WHERE email="{form.email.data}" ')
            result_email=mycur.fetchone()
            if not(result_pw):
                if (not(result_email) and flag):
                    mycur.execute(f"""INSERT INTO reg(user,email,pass)
                    VALUES("{form.username.data}","{form.email.data}","{form.password.data}")""")
                    db.commit()

                    flash(f"""Account created for {form.username.data}!""",'success')
                    session['user']=form.username.data
                    return home()
                else:
                    flash("Account with that email already exists!",'danger')
            else:
                flash("Username taken,try a diffrent one",'danger')
        else:
            flash("""Please use Alpha-numeric[a-z,A-Z,0-9] characters only!""",'danger')
        return render_template('register.htm',
                            form=form,title='Register')
    else:
        return render_template('register.htm',
                            form=form,title='Register')
@app.route("/")
@app.route('/login',methods=['POST','GET'])
def login():
    if session.get('user'):
        return home()
    form=LoginForm()
    if form.validate_on_submit():
        p=re.compile('\W')
        result_reg=p.findall(form.username.data)
        if not(result_reg):
            mycur.execute(f"""SELECT pass FROM reg WHERE user="{form.username.data}" """)
            result=mycur.fetchone()
            if result:
                if form.password.data==result[0]:
                    session['user']=form.username.data
                    flash('Login Successful','success')
                    return home()
                else:
                    flash('Login unsuccessful,please check your password','danger')
            else:
                flash('Account does not exist','danger')  
        else:
            flash('Account does not exist','danger')
    return render_template('login.htm',title='Login',form=form)

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
@app.route("/account")
def account():
    if not(session.get('user')):
        return redirect(url_for('login'))
    mycur.execute(f""" SELECT email FROM reg WHERE user= "{session.get('user')}" """)
    email=mycur.fetchone()[0]
    return render_template('account.htm',email=email)
     

if __name__=='__main__':
    app.run(debug=True)