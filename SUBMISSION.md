# Github Octernship - DiveHQ 

## About

This repository is a Calorie Tracker Web Application built using Django Rest Framework and SQLite3 database.The application allows users to enters their meals and thereby manage their calorie intake. The application also allows managers to keep track of their users <br>
It was developed as a part of the Backend Internship Task for DiveHQ for the Github Octernship program.

## Features
1. Sign up/ Sign in to the Web Application
2. Mantain Calorie intake
3. Set Goals
4. Managers can access their users meals
5. Get Calorie intakes for meals without knowing it
6. Create, Update , See and Delete meal entries

## Repository Setup

1. Clone the repository to your local machine:

   ```
   $ git clone <repository-url>
   ```

2. Navigate to the project directory and change into the backend directory:

   ```
   $ cd <directory>
   ```

3. Create and activate a virtual environment (optional but recommended):

   ```
   $ pipenv shell
   ```

4. Install the required dependencies:

   ```
   $ pip install -r requirements.txt
   ```

5. Set up the database:

   ```
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```

6. (Optional) Create a superuser to access the admin interface:

   ```
   $ python manage.py createsuperuser
   ```

7. Start the development server:

   ```
   $ python manage.py runserver
   ```


8. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to access the project.


9. Go to visit [http://localhost:8000/register](http://localhost:8000/register) to create an account. Only authenticated Users can access the web app
![alt text](https://github.com/DiveHQ-Octernships/dive-backend-engineering-octernship-smeet07/blob/main/calorie_tracker/tracker/images/WhatsApp%20Image%202023-06-19%20at%206.53.52%20PM.jpeg)

10. Use [http://localhost:8000/entries/create](http://localhost:8000/entries/create) to create entries.
![alt text](https://github.com/DiveHQ-Octernships/dive-backend-engineering-octernship-smeet07/blob/main/calorie_tracker/tracker/images/WhatsApp%20Image%202023-06-19%20at%206.56.26%20PM.jpeg)

## Running the API Server Locally
- Run the following command to start the API server:
    ```
    $ python manage.py runserver 8000
    ``` 
    The API server will start, and you can access it at http://localhost:8000/ in your web browser.
    Make sure to replace 8000 with the appropriate port number if you have configured a different port for your Django project.


## Deployment

- Dockerize the Django application (optional but recommended) for easier Development and Deployement.[For reference](https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application)
- You can also refer to the official [Django documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/) for deploying django applications


## Steps to Obtain API Key from USDA FoodData Central API

1. Visit [USDA](https://fdc.nal.usda.gov/api-guide.html) site and sign up for an account.
2. Visit https://fdc.nal.usda.gov/api-key-signup.html and fill the form to get the API Key.
3. The API key will be sent on the email provided.
4. Copy the API key and paste it in the .env file in the project directory.