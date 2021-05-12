from bs4 import BeautifulSoup
import bs4
from time import sleep
from datetime import datetime
import random,string
def test_addCourse(test_client,init_database,login_default_user):
    response=test_client.post('/',data=dict(name="Data Structures",\
    course_code="C123",available_for=[1,2],details="Course on data structures",\
    submit="Add Course"),follow_redirects=True)
    assert response.status_code==200
    soup=BeautifulSoup(response.data,'lxml')
    courses=soup.find_all('a',class_='courseLinks')
    course_names=[a.text for a in courses]
    print(course_names)
    assert "Data Structures" in course_names


def test_addCourseMaterial(test_client,addCourse):
    from pprint import pprint
    pprint(vars(addCourse[0]))

    assert addCourse[0].status_code==200
    title=''.join(random.choice(string.ascii_lowercase) for i in range(10))
    response=test_client.post(addCourse[1],data=dict(title=title,\
    details="Course on data structures, quiz 1",\
    submit1="Submit"),follow_redirects=True)
    soup = BeautifulSoup(response.data, 'lxml')
    assert response.status_code==200
    courseNoteCards=soup.find_all('div',class_='courseNoteCard')
    titles=[a.h5.text.strip() for a in courseNoteCards]
    print(titles)
    assert title in titles

    
    
def test_Assignment(test_client,addCourse):
    from pprint import pprint
    assert addCourse[0].status_code==200
    title=''.join(random.choice(string.ascii_lowercase) for i in range(10))
    response=test_client.post(addCourse[1],data=dict(title=title,\
    details="Course on data structures, assignment 1",deadline="2021-05-15T03:57",\
    submit2="Submit"),follow_redirects=True)
    soup = BeautifulSoup(response.data, 'lxml')
    assert response.status_code==200
    courseNoteCards=soup.find_all('div',class_='assignmentCard')
    titles=[a.h5.text.strip().split()[0] for a in courseNoteCards]
    print(titles)
    assert title in titles

    
def test_professor_view_quiz(test_client, login_default_user):
    response = test_client.get('/course/1/quizzes')
    assert response.status_code == 200
    bs = BeautifulSoup(response.data, 'lxml')
    start = bs.find('h5', class_='start')
    end = bs.find('h5',class_="end")
    q1 = bs.find('a', class_='q1')
    start_time = start.text
    end_time = end.text
    link=q1['href']
    print(response.data)
    response1 = test_client.get(link)
    assert response1.status_code == 200
    assert b'Quiz1' in response.data


def test_professor_create_quiz(test_client, login_default_user):
    response=test_client.post('/course/1/quizzes/create_quiz',data=dict(name="Quiz2",\
        start_time=datetime(2021, 5, 21, 8, 10, 10, 10),end_time=datetime(2021, 5, 21, 8, 11, 10, 10),
        submit="true"),follow_redirects=True)
    assert response.status_code==200
    assert b'Question ?' in response.data
    assert b'Multi Correct Question ?' in response.data
    assert b'Partial Marking ?' in response.data
    assert b'Marks' in response.data
    assert b'Option 1' in response.data
    assert b'Multi Correct Question ?' in response.data
    assert b'Option 2' in response.data
        
        

def test_professor_add_question(test_client, login_default_user):
    response=test_client.post('/course/1/quizzes/1/add_question',data=dict(question="Odd one out",is_multi_correct=False,is_partial=False, 
    marks=2,option1="flask", option2="django", option3="ruby on rails", option4="expressjs", ans='4',
        submit="true"),follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Odd one out' in response.data
    assert b'flask' in response.data
    assert b'django' in response.data
    assert b'ruby on rails' in response.data
    assert b'expressjs' in response.data


    
def test_professor_view_all_questions(test_client, login_default_user):
    response = test_client.get('/course/1/quizzes/1/')
    print(response.data)
    
    assert response.status_code == 200
    # 1st question in quiz
    assert b'Odd one out' in response.data
    assert b'Marks: 2' in response.data
    assert b'flask' in response.data
    assert b'django' in response.data
    assert b'ruby on rails' in response.data
    assert b'expressjs' in response.data

    # 2nd question in quiz
    assert b'Cities in Maharastra' in response.data
    assert b'Marks: 4' in response.data
    assert b'Indore' in response.data
    assert b'Nasik' in response.data
    assert b'Mumbai' in response.data
    assert b'Bombay' in response.data
    

def test_professor_enrollment_request(test_client, login_default_user):
    response = test_client.get('/course/1')
    assert response.status_code == 200
    bs = BeautifulSoup(response.data, 'lxml')
    enroll_req_link = bs.find('a', class_='e1')['href']
    
    response1 = test_client.get(enroll_req_link)
    assert response1.status_code == 200
    assert b'Dipin' in response1.data
    bs = BeautifulSoup(response1.data, 'lxml')
    accept_enroll_req = bs.find('a', class_='e2')['href']
    print(accept_enroll_req)
    
    response2 = test_client.get(accept_enroll_req,follow_redirects=True)
    print("response2 = ")
    print(response2.data)
    assert response2.status_code == 200
    assert b'Enrolled.' in response2.data

def test_discussion(test_client,view_discussion_forum):
    # print(view_discussion_forum[0].data.decode("utf-8"))

    soup = BeautifulSoup(view_discussion_forum[0].data, 'lxml')

    heading=soup.find('h1',id="discussionHeading")
    assert heading is None
    content=''.join(random.choice(string.ascii_lowercase) for i in range(10))
    postResponse=test_client.post(view_discussion_forum[1],data=dict(details=content,submit="Submit"),follow_redirects=True)
    assert postResponse.status_code==200
    soup=BeautifulSoup(postResponse.data, 'lxml')
    posts_list= []
    print("soup.find_all('div', class_='postContent')==>", soup.find_all('div', class_='postContent'))
    for post in soup.find_all('div', class_='postContent'):
        posts_list.append(post.text.strip())

    assert content in posts_list


    content=''.join(random.choice(string.ascii_lowercase) for i in range(10))
    postResponse=test_client.post(view_discussion_forum[1],data=dict(content=content),follow_redirects=True)
    assert postResponse.status_code==200
    soup=BeautifulSoup(postResponse.data, 'lxml')
    posts_list= []
    print("soup.find_all('div', class_='postContent')==>", soup.find_all('div', class_='postContent'))
    for post in soup.find_all('div', class_='postContent'):
        posts_list.append(post.text.strip())

    assert content in posts_list

def test_remove_course(test_client,removeCourse):
    assert removeCourse[0].status_code==200
    assert 'Welcome Professor 1' in removeCourse[1]
    assert 'Welcome to Course Management System' not in removeCourse[1]
    courses_list= []
    soup = BeautifulSoup(removeCourse[0].data, 'lxml')
    for course in soup.find_all('td'):
        if(course.get('a')):
            courses_list.append(course.a.text)

    assert 'Data Structures' not in courses_list