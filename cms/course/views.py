from operator import sub
import pandas as pd
import random
import string
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort,send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import file
from cms import basedir,ALLOWED_EXT,db
from cms.models import Course, Request, User,courseNote,Attachment,Assignment
from .forms import addCourseNote,assignmentForm

from datetime import datetime
from werkzeug.utils import secure_filename
CourseBluerint = Blueprint('course', __name__)
cb=CourseBluerint


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@cb.route('/serve/<filename>')
@login_required
def serve_file(filename):
    return send_from_directory(os.path.join(basedir, '..', '..', 'static_material'), filename=filename, as_attachment=True)


@cb.route('/course/<course_id>',methods=['GET', 'POST'])
@login_required
def view_course(course_id):
    courseToRender=Course.query.filter_by(id=course_id).first()
    courseNoteForm=addCourseNote()
    addAssignmentForm=assignmentForm()
        # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100))
    # details = db.Column(db.String(100))
    # attachments=db.relationship('Attachment',backref='coursenote')
    # course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    # def __init__(self,title,details,course_id):
    #     self.title=title
    #     self.details=details
    # #     self.course_id=course_id
    # title = StringField('Note Title', validators=[DataRequired('Data required')])
    # details = StringField('Details', validators=[DataRequired('Data required')])
    if courseNoteForm.submit1.data and courseNoteForm.validate:
        attachments=[]
        if not current_user.is_authenticated:
            abort(405)
        newCourseNote=courseNote(courseNoteForm.title.data,courseNoteForm.details.data,course_id=course_id)
        db.session.add(newCourseNote)
        db.session.commit()

        if courseNoteForm.attachments.data:
            print(courseNoteForm.attachments.data,request.files)
            for uploaded_file in request.files.getlist('attachments'):

                filename, file_extension = os.path.splitext(uploaded_file.filename)
                savename = secure_filename(filename)+''.join(
                    random.choice(string.ascii_lowercase) for i in range(16))+file_extension
                print(filename,savename)
                if savename=="":
                    break
                
                uploaded_file.save(os.path.join(basedir, '..', '..', 'static_material', savename))
                new_attachment = Attachment(
                    filename, file_extension,url_for('course.serve_file',filename=savename),newCourseNote.id)
                attachments.append(new_attachment)
        print(attachments)

        db.session.add_all(attachments)
        db.session.commit()
        return redirect(url_for('course.view_course',course_id=course_id))




    
    if addAssignmentForm.submit2.data and addAssignmentForm.validate:
        attachments=[]
        if not current_user.is_authenticated:
            abort(405)
        newAssignment=Assignment(addAssignmentForm.title.data,addAssignmentForm.details.data,addAssignmentForm.deadline.data,course_id=course_id)
        print('asdasdasdasd')
        db.session.add(newAssignment)
        db.session.commit()

        if addAssignmentForm.attachments.data:
            print(addAssignmentForm.attachments.data,request.files)
            for uploaded_file in request.files.getlist('attachments'):

                filename, file_extension = os.path.splitext(uploaded_file.filename)
                savename = secure_filename(filename)+''.join(
                    random.choice(string.ascii_lowercase) for i in range(16))+file_extension
                print(filename,savename)
                if savename=="":
                    break
                
                uploaded_file.save(os.path.join(basedir, '..', '..', 'static_material', savename))
                new_attachment = Attachment(
                    filename, file_extension,url_for('course.serve_file',filename=savename),assignment_id=newAssignment.id)
                attachments.append(new_attachment)
        print(attachments)

        db.session.add_all(attachments)
        db.session.commit()
        return redirect(url_for('course.view_course',course_id=course_id))
    


    return render_template('view_course.html',course=courseToRender,courseNoteForm=courseNoteForm,addAssignmentForm=addAssignmentForm)





@cb.route('/course/drop/<course_id>')
@login_required
def remove(course_id):
    courseToDrop = Course.query.filter_by(id=course_id).first()
    db.session.delete(courseToDrop)
    db.session.commit()
    return redirect(url_for('core.index'))


@cb.route('/coursenote/delete/<courseNote_id>')
@login_required
def remove_courseNote(courseNote_id):
    courseNotetoDelete=courseNote.query.filter_by(id=courseNote_id).first()
    course_id=courseNotetoDelete.course.id
    if(current_user!=courseNotetoDelete.course.professor):
        flash('Not authenticated')
        abort(405)
    cnd=courseNotetoDelete
    if cnd.attachments:
        for attachment in cnd.attachments:
            file_path = os.path.join(
                basedir, "..", "..", "static_material", os.path.basename(attachment.link))
            if os.path.isfile(file_path):
                os.remove(file_path)
            db.session.delete(attachment)
    db.session.delete(cnd)
    db.session.commit()
    return redirect(url_for('course.view_course',course_id=course_id))


@cb.route('/assignment/delete/<assignment_id>')
@login_required
def remove_assignment(assignment_id):
    courseNotetoDelete=Assignment.query.filter_by(id=assignment_id).first()
    course_id=courseNotetoDelete.course.id
    if(current_user!=courseNotetoDelete.course.professor):
        flash('Not authenticated')
        abort(405)
    cnd=courseNotetoDelete
    if cnd.attachments:
        for attachment in cnd.attachments:
            file_path = os.path.join(basedir, "..", "..", "static_material", os.path.basename(attachment.link))
            if os.path.isfile(file_path):
                os.remove(file_path)
            db.session.delete(attachment)
    if cnd.submissions:
        for submission in cnd.submissions:
            if submission.attachments:
                for attachment in submission.attachments:
                    file_path = os.path.join(
                        basedir, "..", "..", "static_material", os.path.basename(attachment.link))
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    db.session.delete(attachment)
                db.session.delete(submission)

    db.session.delete(cnd)
    db.session.commit()
    return redirect(url_for('course.view_course',course_id=course_id))


@cb.route('/course/<course_id>/export')
@login_required
def export_students_course(course_id:int):
    course=Course.query.filter_by(id=course_id).first()
    if not course or current_user != course.professor:
        abort(404)
    students=course.students
    df=pd.DataFrame.from_records([s.to_dict() for s in students],index='id')
    print(df)
    savename = str(course.name) + \
        datetime.now().strftime("%Y-%m-%d_%H:%M")+'.xlsx'
    savename=secure_filename(savename)
    df.to_excel(os.path.join(basedir, '..', '..', 'temp',savename),index=True)
    return send_from_directory(os.path.join(basedir, '..', '..', 'temp'), filename=savename, as_attachment=True)



@cb.route('/course/<assignment_id>/submissions')
@login_required
def view_assignment_submissions(assignment_id:int):
    assignment=Assignment.query.filter_by(id=assignment_id).first()
    if not assignment or current_user != assignment.course.professor:
        abort(404)
    
    submissions=assignment.submissions
    return render_template('view_submissions.html',submissions=submissions,assignment=assignment)


@cb.route('/course/<course_id>/requests')
@login_required
def view_requests(course_id: int):
    workingCourse=Course.query.filter_by(id=course_id).first()
    if not workingCourse or workingCourse.professor!=current_user:
        abort(401)
    requests=workingCourse.requests 
    return render_template('view_requests.html', requests=requests)



@cb.route('/course/requests/accept/<request_id>')
@login_required
def request_accept(request_id: int):
    workingRequest=Request.query.filter_by(id=request_id).first()
    if not workingRequest or workingRequest.course.professor!=current_user:
        abort(401)
    workingRequest.user.courses.append(workingRequest.course)
    workingRequest.status=1
    db.session.commit()
    return redirect(url_for('course.view_requests',course_id=workingRequest.course.id))


@cb.route('/course/requests/decline/<request_id>')
@login_required
def request_decline(request_id: int):
    workingRequest = Request.query.filter_by(id=request_id).first()
    if not workingRequest or workingRequest.course.professor != current_user:
        abort(401)
    workingRequest.status=2
    db.session.commit()
    return redirect(url_for('course.view_requests', course_id=workingRequest.course.id))
