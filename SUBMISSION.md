# Calorie API 

# Assumptions
This API is built with the following assumptions:

The API is designed to provide CRUD (Create, Read, Update, Delete) operations for user entries, where each entry has a date, time, text, and number of calories.
If the number of calories is not provided, the API will connect to the Nutritionix API to retrieve the number of calories for the entered meal.
Each user has an expected number of calories per day, and the API will determine if the total calories for a given day are below or above this expected number.
The API supports authentication and implements role-based access control. There are three roles: regular user, user manager, and admin. Each role has different permission levels.

## Getting Started

To get started with the  API, follow these steps:

### Clone the Repository

Clone the repository to your local machine using the following command:

```shell
git clone <repository_url>
```
Set Up Dependencies
1. Navigate to the project's root directory:
```shell
cd dummyapi
```
Create a virtual environment (optional but recommended):

```shell
python3 -m venv venv
``
Activate the virtual environment:

For Linux/macOS:
```shell
source venv/bin/activate
```
For Windows:
```shell
venv\Scripts\activate
```
Install the required dependencies:

```shell
pip install -r requirements.txt
```
Run the Test Suite
To run the test suite, execute the following command:
```shell
python -m pytest app/tests
```
This will run both the unit tests and integration tests and display the test results.

Start the API Server
To start the API server, use the following command:

```shell
flask run
```
```shell
The API server will be running locally at http://localhost:5000/.
```
API Endpoints
The Dummy API provides the following endpoints:

1. User Registration: POST /api/auth/register
2. User Login: POST /api/auth/login
3. Create Entry: POST /api/entries
4. Get All Entries: GET /api/entries
5. Get Entry by ID: GET /api/entries/{entry_id}
6. Update Entry: PUT /api/entries/{entry_id}
7. Delete Entry: DELETE /api/entries/{entry_id}
8. Please replace {entry_id} with the ID of the entry you want to access or modify.