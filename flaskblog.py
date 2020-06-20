from flask import Flask,render_template,redirect,url_for,request,flash,session
from forms import RegistrationForm,LoginForm,PostForm,UpdateForm
import mysql.connector as sq
import re
import datetime
from flask_bcrypt import Bcrypt
import secrets
import os


db=sq.connect(
    host="localhost",
    user="root",
    passwd="Nasamud@yahoopee5216",
    database="flask"
)
mycur=db.cursor()

app=Flask(__name__)
app.config['SECRET_KEY']='27850d1f47f1aef5a288f142'
crypt=Bcrypt(app)


@app.route('/home')
def home():
    if not(session.get('user')):
        return redirect(url_for('login'))
    author=session.get('user')
    mycur.execute(f""" SELECT title,content,author,date_ FROM posts WHERE author <> %s ORDER BY date_ DESC """,(author,))
    posts=mycur.fetchall()
    return render_template("home.htm",title="home",posts=posts,current_add='home') 

@app.route('/write',methods=['GET','POST'])
def write():
    if not(session.get('user')):
        return redirect(url_for('login'))
    form=PostForm()
    if form.validate_on_submit():
        now = datetime.datetime.now().strftime("%Y-%m-%d")
      
        mycur.execute(f"""INSERT INTO posts(title,content,author,date_)
        VALUES(%s,%s,%s,%s)""",(form.title.data,form.Text.data,session.get('user'),now))
        db.commit()
        flash('Post created,cool!','success')

    return render_template('write.htm',
                            title="write",form=form,current_add='write')

@app.route("/register",methods=['GET','POST'])
def register():
    if session.get('user'):
        return home()
    form=RegistrationForm()
    if form.validate_on_submit():
    
        mycur.execute(f'SELECT * FROM reg WHERE user= %s ',(form.username.data,))
        result_pw=mycur.fetchone()
        mycur.execute(f'SELECT * FROM reg WHERE email=%s ',(form.email.data,))
        result_email=mycur.fetchone()
        if not(result_pw):
            if not(result_email):
                password=crypt.generate_password_hash(form.password.data).decode('utf-8')
                mycur.execute(f"""INSERT INTO reg(user,email,pass)
                VALUES(%s,%s,%s)""",(form.username.data,form.email.data,password))
                db.commit()
                flash(f"""Account created for {form.username.data}!""",'success')
                session['user']=form.username.data
                return home()
            else:
                flash("Account with that email already exists!",'danger')
        else:
            flash("Username taken,try a diffrent one",'danger')
    return render_template('register.htm',
                            form=form,title='Register',current_add='register')
@app.route("/")
@app.route('/login',methods=['POST','GET'])
def login():
    if session.get('user'):
        return home()
    form=LoginForm()
    if form.validate_on_submit():
    
        mycur.execute(f"""SELECT pass FROM reg WHERE user=%s """,(form.username.data,))
        result=mycur.fetchone()
        if result:
            if crypt.check_password_hash(result[0],form.password.data):
                session['user']=form.username.data
                flash('Login Successful','success')
                return home()
            else:
                flash('Login unsuccessful,please check your password','danger')
        else:
            flash('Account does not exist','danger')  
    return render_template('login.htm',title='Login',form=form,current_add='login')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
@app.route("/account",methods=['POST','GET'])
def account():
    if not(session.get('user')):
        return redirect(url_for('login'))
    form=UpdateForm()
    if form.validate_on_submit():
        mycur.execute(f'SELECT * FROM reg WHERE user= %s ',(form.username.data,))
        result_user=mycur.fetchone()
        mycur.execute(f'SELECT * FROM reg WHERE email=%s ',(form.email.data,))
        result_email=mycur.fetchone()
        if not(result_user):
            if not(result_email):
                
                if form.email.data:
                    mycur.execute(""" UPDATE reg SET email = %s WHERE user = %s """,(form.email.data,session.get('user')))
                    db.commit()
                if form.username.data:
                    mycur.execute(""" SET FOREIGN_KEY_CHECKS =0 """ )
                    mycur.execute(""" UPDATE reg SET user = %s WHERE user = %s """,(form.username.data,session.get('user')))
                    mycur.execute(""" UPDATE posts SET author = %s WHERE author = %s """,(form.username.data,session.get('user')))
                    mycur.execute(""" SET FOREIGN_KEY_CHECKS =1 """ )
                    db.commit()
                    session['user']=form.username.data
                if form.dp.data:
                    mycur.execute(f""" SELECT image_file FROM reg WHERE user= %s """,(session.get('user'),))
                    image_file=mycur.fetchone()[0]
                    file_path=os.path.join(app.root_path,'static\profile_pics',image_file)
                    os.remove(file_path)
                    picture=save(form.dp.data)
                    mycur.execute(""" UPDATE reg SET image_file = %s where user = %s """,(picture,session.get('user')))
                    db.commit()
                flash('changed Successfully','success')
            else:
                flash("Account with that email already exists!",'danger')
        else:
            flash("Username taken,try a diffrent one",'danger')
            
    mycur.execute(f""" SELECT email,image_file FROM reg WHERE user= %s """,(session.get('user'),))
    email,image_file=mycur.fetchone()
    profile_pic=url_for('static',filename='profile_pics/'+image_file)
    return render_template('account.htm',email=email,form=form,current_add='account',dp=profile_pic)

def save(photo):
    _,file_ext=os.path.splitext(photo.filename)
    random=secrets.token_hex(8)
    file_nm=random+file_ext
    file_path=os.path.join(app.root_path,'static\profile_pics',file_nm)
    photo.save(file_path)
    return file_nm

     

if __name__=='__main__':
    app.run(debug=True)