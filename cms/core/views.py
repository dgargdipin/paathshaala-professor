from flask.helpers import url_for
from cms import db
from operator import add
from flask import render_template, request,Blueprint,redirect,abort
from cms.professor.forms import addCourseForm
from cms.models import Course,Branch
core=Blueprint('core',__name__)
from flask_login import current_user
print("__name__ is ",__name__)


@core.route('/',methods=['GET', 'POST'])
def index():
    form=addCourseForm()
    courses=None
    if current_user.is_authenticated:
        courses=current_user.courses
    

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            abort(405)
        new_course=Course(name=form.name.data,course_code=form.course_code.data,details=form.details.data,prof_id=current_user.id)
        print(form.available_for.data)

        for branch_code in form.available_for.data:
            branch=Branch.query.filter_by(id=branch_code).first()
            print(branch)
            if branch is not None:
                new_course.branches.append(branch)
        db.session.add(new_course)
        db.session.commit()
        print("courses", current_user.courses)
        return redirect(url_for('core.index'))
    if form.submit():
        print(form.available_for.data)
        return render_template('index.html', form=form, courses=courses)
    return render_template('index.html',form=form,courses=courses)

@core.route('/info')
def info():
    return render_template('info.html')
