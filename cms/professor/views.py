# register user
#login user
#logout user
# account update UserForm)

from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash
from cms import db
from cms.models import Professor
from cms.professor.forms import RegistrationForm,LoginForm,UpdateProfForm
professors=Blueprint('professors',__name__)

@professors.route('/register',methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        # user_data={k:v.data for k,v in form}
        # print(user_data)
        print(form)
        professor=Professor(form.name.data,form.email.data,form.password.data,form.branch.data)
        db.session.add(professor)
        db.session.commit()
        flash('Thanks for registration!','primary')
        return redirect(url_for('professors.login'))
    return render_template('register.html',form=form)

@professors.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user =Professor.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next=request.args.get('next')
            if next==None or not next[0]=='/':
                next=url_for('core.index')
            return redirect(next)
        elif user is None:
            flash('E-Mail not found','danger')
        else:
            flash('Password incorrect','danger')
    return render_template('login.html',form=form)


@professors.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@professors.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfForm()
    if form.validate_on_submit():

        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.password_hash = generate_password_hash(
                form.password.data)
        db.session.commit()
        flash('User account updated','primary')
        return redirect(url_for('professors.account'))
    elif request.method == "GET":
        form.email.data = current_user.email
    return render_template('account.html', form=form)
