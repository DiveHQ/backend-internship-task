# DiveHQ - Backend Internship Task

This is a Django Rest Framework based backend for a Calorie Tracker Application. The application allows users to track their calorie intake. The application also allows users to set goals for themselves. <br>
It was developed as a part of the Backend Internship Task for DiveHQ.

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

8. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to see the project in action.

### Configuration

- Modify the project settings in `settings.py` as needed, such as database settings, static files, etc.

## Running the Test Suite

- Run the tests to make sure everything is working correctly:

   ```
   $ python manage.py test
   ```
   This command will run all the tests and display the results in the console.

## Running the API Server
- Run the following command to start the API server:
    ```
    $ python manage.py runserver 8000
    ``` 
    The API server will start, and you can access it at http://localhost:8000/ in your web browser or via API clients like cURL or Postman.
    Make sure to replace 8000 with the appropriate port number if you have configured a different port for your Django project.


## Deployment

- Refer to the official Django documentation for instructions on deploying Django projects to production environments.

## API Documentation

[Postman Collection](https://interstellar-crescent-487348.postman.co/workspace/TICC~f2c8121f-3c6e-4f37-8235-c8fdd6b5a5b4/collection/17375194-b95733eb-afb2-49a0-a1c1-417f71896177?action=share&creator=17375194) <br>
[Restframework Docs](http://127.0.0.1:8000/doc/) <br>
[Redoc](http://127.0.0.1:8000/redoc/) <br>
[To download API documentation in Yaml](http://127.0.0.1:8000/doc.yaml) <br>
[To view API documentation in json](http://127.0.0.1:8000/doc.json) 


## Obtaining API Key from calorieNinjas

1. Visit [calorieninjas](https://calorieninjas.com/) and sign up for an account.
2. After verifying your email, visit [calorieninjas](https://calorieninjas.com/) again and login to your account.
3. Click on the **API** tab on the left sidebar.
4. Copy the API key and paste it in the .env file in the project directory.