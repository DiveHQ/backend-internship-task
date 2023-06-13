# Project Submission

## Project Setup

To set up the repository and install the dependencies, please follow these steps:

1. Clone the repository:
git clone https://github.com/DiveHQ/backend-internship-task.git
cd backend-internship-task

2. Create and activate a virtual environment:
python3 -m venv env
source env/bin/activate (Linux/Mac)
env\Scripts\activate (Windows)

3. Install the required dependencies:
pip install -r requirements.txt

cd caloriesapi

4. Apply the database migrations:
python manage.py migrate

## Running the Test Suite

To run the unit tests and end-to-end tests, use the following command:
python manage.py test

## Running the API Server

To start the API server, execute the following command:
python manage.py runserver

The API server will be accessible at `http://localhost:8000/api/`.

## Additional Notes

- Make sure to update the `NUTRTIONIX_API_KEY` and `NUTRTIONIX_APP_ID` variable in the Django settings with your own API key and app id for retrieving calorie information from an external API.