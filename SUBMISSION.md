
#best to hava a virtual environment
- [ ] commands to set up the repo (dependencies etc.)

-clone https://github.com/DiveHQ/backend-internship-task.git
-run pip install requirement.txt {
    if errors:
        manually:
            *pip install django
            *pip install djangorestframework
            *pip install django-rest-knox
}

-python manager migrate 
-python manager createsuperuser(create admin)
#now kick start the server(welcome)
-python manage.py runserver

#commands to run the test suite

1.python manage.py test authen.tests.ViewTesting.test_register  
2.python -Wa manage.py test authen.tests.ViewTesting.test_login --keepdb

"""
with the user manager and the Calories endpoint testing, i decided to test agaisnt the 401 status
code because in django testing is not allow with the production database.Hence i could not get the right Auth Token for the test

But in other be sure that it work i used postman to re test the endpoints

"""
#for the user manager

1.python -Wa manage.py test authen.tests_umanager.View_Manager_Test.test_GetUser 
2.python -Wa manage.py test authen.tests_umanager.View_Manager_Test.test_DeleteUser
3.python -Wa manage.py test authen.tests_umanager.View_Manager_Test.test_UpdateUser
4.python -Wa manage.py test authen.tests_umanager.View_Manager_Test.test_CreateUser

#for the calories

1.python -Wa manage.py test calori.test_viewp.ViewTestCase.test_get
2.python -Wa manage.py test calori.test_viewp.ViewTestCase.test_post
3.python -Wa manage.py test calori.test_viewp.ViewTestCase.test_delete 
4.python -Wa manage.py test calori.test_viewp.ViewTestCase.test_update  

#to run all test,
1..python  manage.py test



#commands to run the API server

python manage.py runserver


<INTRUCTION>
#there is the need to get an nutrition api key from
https://api.api-ninjas.com

and save it as secret.json in the basePath where manage.py is
Storing in the form {
    "API_KEY":"Your_API_KEY"
}
will make it simple for you


<NOTICE>

THERE IS A TEST THAT FAILS, AND AM STILL WORKING ON THE LOGIC

