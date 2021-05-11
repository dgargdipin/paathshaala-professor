from werkzeug import test
import pytest
from cms import app, db
from datetime import datetime
from cms.models import User,Professor, Course, Quiz, Question, Option, Request

import cms.branch_helper as branch_helper


@pytest.fixture(scope='module')
def new_user():
    user = Professor("Professor 2","prof2@gmail.com","prof2",1)
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    # Insert user data
    db.create_all()
    db.session.add_all(branch_helper.create_branch_array())
    db.session.commit()

    user1 = User('Dipin','dgargdipin@gmail.com','abc','1',1)
    user2 = Professor("Professor 1","prof1@gmail.com","prof1",2)
    # user_other_branch = User('Ram', 'ram@gmail.com', 'abc', '1', 2)
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    course = Course(details="Course on Data structures", prof_id=user2.id, name="Data structures", course_code='203', 
        can_apply=True)
    db.session.add(course)
    db.session.commit()

    quiz = Quiz(course_id= course.id,name="Quiz1",start_time= datetime(2015, 6, 5, 8, 10, 10, 10), end_time=datetime(2015, 6, 5, 8, 10, 12, 10))
    db.session.add(quiz)
    db.session.commit()

    # Adding two Question in Quiz1
    question1 = Question(quiz_id=quiz.id, question="Odd one out", ans='4', marks=2, is_multicorrect=True , is_partial=True)
    question2 = Question(quiz_id=quiz.id, question="Cities in Maharastra", ans='2,3,4', marks=4, is_multicorrect=True , is_partial=True)
    db.session.add(question1)
    db.session.add(question2)
    db.session.commit()

    # Options for 1st question
    option1 = Option(question_id=question1.id, option='django', is_right=False)
    option2 = Option(question_id=question1.id, option='flask', is_right=False)
    option3 = Option(question_id=question1.id, option='ruby on rails', is_right=False)
    option4 = Option(question_id=question1.id, option='expressjs', is_right=True)
    db.session.add(option1)
    db.session.add(option2)
    db.session.add(option3)
    db.session.add(option4)
    db.session.commit()

    # Options for 2nd question
    option1 = Option(question_id=question2.id, option='Indore', is_right=False)
    option2 = Option(question_id=question2.id, option='Nasik', is_right=True)
    option3 = Option(question_id=question2.id, option='Mumbai', is_right=True)
    option4 = Option(question_id=question2.id, option='Bombay', is_right=True)
    db.session.add(option1)
    db.session.add(option2)
    db.session.add(option3)
    db.session.add(option4)
    db.session.commit()
    

    # Request for enrollment in course
    req = Request(user_id=user1.id, course_id=course.id, title="Request to Access Course", details="Please allow me!!")
    db.session.add(req)
    db.session.commit()
    
    yield# this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module')
def login_default_user(test_client,init_database):
    test_client.post('/login',
                     data=dict(email='prof1@gmail.com', password='prof1'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)


from bs4 import BeautifulSoup
import bs4

@pytest.fixture(scope='module')
def addCourse(test_client,init_database,login_default_user):
    response=test_client.post('/',data=dict(name="Data Structures",\
    course_code="C123",available_for=[1,2],details="Course on data structures",\
    submit="Add Course"),follow_redirects=True)
    assert response.status_code==200
    soup=BeautifulSoup(response.data,'lxml')
    courses=soup.find_all('a',class_='courseLinks')
    course_names=[a.text for a in courses]
    print(course_names)
    url=""
    assert "Data Structures" in course_names
    for course in courses:
        if course.text=="Data Structures":
            url=course['href']
            response=test_client.get(url)
            break
    yield response,url

@pytest.fixture(scope='module')
def view_discussion_forum(test_client,addCourse):
    print("viewing discussion forum")
    response=test_client.get(addCourse[1],follow_redirects=True)
    assert response.status_code==200
    soup=BeautifulSoup(response.data,'lxml')
    discussion_a = soup.find('a', id="viewDiscussionForum")
    assert discussion_a is not None
    response=test_client.get(discussion_a['href'],follow_redirects=True)
    assert response.status_code==200
    yield response,discussion_a['href']

@pytest.fixture(scope='module')
def removeCourse(test_client,init_database,login_default_user,addCourse):
    print("removing database")
    response=test_client.get('/course/drop/1',follow_redirects=True)
    assert response.status_code==200
    soup=BeautifulSoup(response.data,'lxml')
    greet = soup.find('div', class_='jumbotron').h1.text
    print("removed database")
    yield response, greet