# DiveHQ - Backend Internship Assignment

This is a Django Rest Framework based backend for a Calorie Tracker Application. The application allows users to track their calorie intake. The application also allows users to set goals for themselves. <br>
It was developed as a part of the Backend Internship Task for DiveHQ.

## Repository Setup

1. Clone the repository to your local machine:

   ```
   $ git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   $ cd <directory>
   ```

3. Install the required dependencies:

   ```
   $ pip install -r requirements.txt
   ```

4. Set up the database:

   ```
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```

5. Create a superuser to access the admin interface:

   ```
   $ python manage.py createsuperuser
   ```

6. Start the development server:

   ```
   $ python manage.py runserver
   ```

7. Open your web browser and visit [http://localhost:8000//api/v1/accounts/register/](http://localhost:8000/api/v1/accounts/register/) . Here you need to register yourself first in order to access the routes.

### Configuration

- Modify the project settings in `settings.py` as needed, such as database settings, static files, etc. If hosted, remember to add the host address in the setting.py file.

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

[Postman Collection](https://documenter.getpostman.com/view/21453554/2s93sjU935)
[API Documentation (.md)](./APIDocumention.md)
