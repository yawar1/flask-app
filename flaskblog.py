from flask import Flask,render_template,redirect,url_for,request,flash
from forms import RegistrationForm,LoginForm


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
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
        
    else:
        
        return render_template('register.htm',
                            form=form,title='Register')

@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='yawarmushtaq52@gmail.com' and form.password.data=='12345':
            flash('Login Successful','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful,please check your email and/or password','danger')
    return render_template('login.htm',title='Login',form=form)
     

if __name__=='__main__':
    app.run(debug=True)