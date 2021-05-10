from bs4 import BeautifulSoup
import bs4
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

    
    


