# Calorie Tracker Application

## Description
The Calorie Tracker is a web application that allows users to track their daily calorie intake by creating and managing entries.

## Setup
1. Clone the repository: 
    git clone https://github.com/DiveHQ-Octernships/dive-backend-engineering-octernship-asifrahaman13.git
2. Navigate to the project directory: 
    
3. Create a virtual environment:
    python -m venv venv
4. Activate the virtual environment:
    - For Windows:
    ```
    venv\Scripts\activate
    ```
    - For macOS/Linux:
    ```
    source venv/bin/activate
    ```
5. Install the required dependencies:
    pip install -r requirements.txt
6. Set up the database:
    - Modify the database connection settings in `main.py` according to your database configuration.

## Usage
1. Start the application server:
    uvicorn main:app --reload
2. Access the application in your web browser at `http://localhost:8000`.

## API Testing with pytest
1. Make sure the application server is running.
2. Activate the virtual environment if not already activated.
3. Run the pytest cases:
    pytest



## Example usage through Postman or Thunder Client

Getting started:

URL: http://0.0.0.0:8000/

REQUEST TYPE:

GET

RESPONSE:

Hello, world!
************************************************************************************************
Now first, you need to register before being able to use the app.

URL: http://0.0.0.0:8000/api/register

Request Type: POST

JSON PALOAD:

{ 
  "username":"asifxy",
  "password":"pass",
  "role":"admin",
  "daily_calorie_goal":120
}

Response:

{
  "status_code": 202,
  "message": "User registered successfully"
}

************************************************************************************************

Next, you need to log in

URL: http://0.0.0.0:8000/api/login

Request Type: POST

JASON PAYLOAD:

{ 
  "username":"asifxyz",
  "password":"pass"
}


Response:

{
  "message": "Login successful"
}

************************************************************************************************

Next, you can enter the entries.

URL: http://0.0.0.0:8000/api/entries

Request Type:  POST

JSON:

{ "date": "2023-06-18",
  "time": "12:00",
  "text": "I Love Apples Oranges",
  "calories": 300,
  "username":"asifxyz",
  "password":"pass",
  "role":"admin",
  "daily_calorie_goal":120
}

Response:

{
  "message": "Entry created successfully"
}

************************************************************************************************

Next you can get all the entries:

URL: http://0.0.0.0:8000/api/entries

REQUEST TYPE: GET

JSON PAYLOAD:

{ "date": "2023-06-18",
  "time": "12:00",
  "text": "I Love Apples Oranges",
  "calories": 300,
  "username":"asifxyz",
  "password":"pass",
  "role":"admin",
  "daily_calorie_goal":120
}

Response:

[
  {
    "time": "12:00:00",
    "id": 6,
    "calories": 500,
    "date": "2023-06-18",
    "user_id": 2,
    "text": "Test entry",
    "is_below_goal": true
  },
  {
    "time": "12:00:00",
    "id": 7,
    "calories": 500,
    "date": "2023-06-18",
    "user_id": 2,
    "text": "Test entry",
    "is_below_goal": true
  },
  {
    "time": "12:00:00",
    "id": 8,
    "calories": 300,
    "date": "2023-06-18",
    "user_id": 6,
    "text": "I Love Apples Oranges",
    "is_below_goal": false
  }
]


************************************************************************************************

To update the details, you need to pass the id of the entry as a slug

URL: http://0.0.0.0:8000/api/entries/8

REQUEST TYPE: PUT

JSON PAYLOAD:

{ "date": "2023-06-18",
  "time": "12:00",
  "text": "I Love Apples only",
  "calories": 300,
  "username":"asifxy",
  "password":"pass",
  "role":"admin",
  "daily_calorie_goal":120
}

RESPONSE:

{
  "message": "Entry updated successfully"
}

To delete, we also need to pass the id in the form of a slug

************************************************************************************************

URL: http://0.0.0.0:8000/api/entries/8

REQUEST TYPE: DELETE]

RESPONSE:

{
  "message": "Entry deleted successfully"
}

We can test similar functionalities for other access rights like amin, users etc. 
