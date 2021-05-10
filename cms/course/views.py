from operator import sub
import pandas as pd
import random
import string
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort,send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import file
from cms import basedir,ALLOWED_EXT,db
from cms.models import Course, QuizResponse, Request, User,courseNote,Attachment,Assignment, Quiz, Question, Option
from .forms import addCourseNote,assignmentForm, quizForm, questionForm

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
                if not filename or not file_extension:
                    continue
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
                if not filename or not file_extension:
                    continue
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
    if not course or current_user != course.professor or not course.students:
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


@cb.route('/course/<course_id>/quizzes/create_quiz/', methods=['GET', 'POST'])
@login_required
def create_quiz(course_id: int):
    course = Course.query.filter_by(id=course_id)
    if not course:
        abort(405)
    quiz_form = quizForm()
    if request.method == 'POST' and quiz_form.validate:
        quiz = Quiz(course_id=course_id, name=quiz_form.name.data, start_time=quiz_form.start_time.data,
                    end_time=quiz_form.end_time.data)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('course.add_question_to_quiz', course_id=course_id, quiz_id=quiz.id))
    return render_template('create_quiz.html', quiz_form=quiz_form)


@cb.route('/course/<course_id>/quizzes')
@login_required
def all_quizzes(course_id: int):
    course = Course.query.filter_by(id=course_id)
    if not course:
        abort(405)
    course = course.first()
    return render_template('all_quizzes.html', quizzes=course.quizzes, course_id=course.id)


@cb.route('/course/<course_id>/quizzes/<quiz_id>/')
@login_required
def display_quiz(course_id: int, quiz_id: int):
    course = Course.query.filter_by(id=course_id)
    if not course:
        abort(405)
    quiz = Quiz.query.filter_by(id=quiz_id)
    if not quiz:
        abort(405)
    quiz = quiz.first()
    bool_values = []
    for question in quiz.questions:
        cur_bool_values = [False, False, False, False]
        for a in question.ans:
            if a == '1':
                cur_bool_values[0] = True
            elif a == '2':
                cur_bool_values[1] = True
            elif a == '3':
                cur_bool_values[2] = True
            elif a == '4':
                cur_bool_values[3] = True
        bool_values.append(cur_bool_values)
    return render_template('display_quiz.html', questions=quiz.questions, course_id=course_id, quiz_id=quiz_id,
                           bool_values=bool_values)


@cb.route('/course/<course_id>/quizzes/<quiz_id>/add_question', methods=['GET', 'POST'])
@login_required
def add_question_to_quiz(course_id: int, quiz_id: int):
    quiz = Quiz.query.filter_by(id=quiz_id)
    if not quiz:
        abort(405)
    question_form = questionForm()
    if request.method == 'POST' and question_form.validate:
        question = Question(quiz_id=quiz_id, question=question_form.question.data, marks=question_form.marks.data,
                            is_multicorrect=question_form.is_multi_correct.data,is_partial=question_form.is_partial.data)
        db.session.add(question)
        db.session.commit()
        numOptions=4
        options_right = [False]*numOptions
        print(options_right)
        mList = [int(e) if e.isdigit()
                 else e for e in question_form.ans.data.split(',')]

        for a in mList:
            if(a>numOptions):abort(405)
            print(a)
            options_right[a-1]=True
        print(options_right)

        options_arr=[]
        for i in range(numOptions):
            option = Option(question_id=question.id, option=getattr(
                question_form, f"option{i+1}").data, is_right=options_right[i])
            print(options_right[i])
            options_arr.append(option)

            db.session.add(option)
            db.session.commit()
            print(option.id,option.is_right)
        # db.session.add_all(options_arr)
        # db.session.commit()
        idlist=[]
        for option in options_arr:
            if option.is_right:
                print(option.option)
                idlist.append(option.id)
        
        question.ans = ','.join(str(v) for v in idlist)
        print(question.ans)
        db.session.commit()
        return redirect(url_for('course.display_quiz', course_id=course_id, quiz_id=quiz_id))
    return render_template('add_question.html', question_form=question_form)


@cb.route('/display/quiz/<attempt_id>')
@login_required
def display_attempt(attempt_id):
    user_response = QuizResponse.query.get_or_404(attempt_id)
    if current_user != user_response.quiz.course.professor:
        abort(405)

    return render_template('display_attempt.html', attempt=user_response, zip=zip)
    # return render_template('display_quiz.html', questions=quiz.questions, course_id=course_id, quiz_id=quiz_id,
    #    bool_values=bool_values)



@cb.route('/display/quiz/<quiz_id>/all')
@login_required
def display_attempts(quiz_id):
    quiz=Quiz.query.get_or_404(quiz_id)
    if current_user!=quiz.course.professor:
        abort(405)
    
    return render_template('display_all_attempts.html', quiz=quiz)
    # return render_template('display_quiz.html', questions=quiz.questions, course_id=course_id, quiz_id=quiz_id,
    #    bool_values=bool_values)


