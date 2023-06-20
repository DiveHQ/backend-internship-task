## ![Dive logo](https://user-images.githubusercontent.com/424487/219708981-f0416526-ba48-4b01-b5b3-c0eb73362718.png) Dive 

## Deployment
The application is deployed on Vercel: `https://api-calories-drf.vercel.app`

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
   $ poetry install
   ```

4. Install the required dependencies and setup database:

   ```
   $ poetry run ./build.sh
   ```

5. Startup the server:

   ```
   $ poetry run ./manage.py runserver
   ```

6. (Optional) Create a superuser to access the admin interface:

   ```
   $ poetry run ./manage.py createsuperuser
   ```

8. Open web browser and visit [http://localhost:8000/](http://localhost:8000/) to access the project.


9. Go to visit [http://localhost:8000/user/register](http://localhost:8000/user/register) to create an account. Only authenticated Users can access the web app

10. Use [http://localhost:8000/tracker/](http://localhost:8000/tracker/) to create and view entries.

## Running the API Server Locally
- Run the following command to start the API server:
    ```
    $ python manage.py runserver 8000
    ``` 
    The API server will start, and you can access it at http://localhost:8000/ in your web browser.
    Make sure to replace 8000 with the appropriate port number if you have configured a different port for your Django project.
