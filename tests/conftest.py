from werkzeug import test
import pytest
from cms import app, db
from cms.models import User,Professor

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
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
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
