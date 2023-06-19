## API Documentation

The backend API provides the following endpoints:

### User Endpoints

#### Register User

- URL: `/api/v1/accounts/register/`
- Method: POST
- Description: Creates a new user account.
- Request Body:
  - `username` (string, required): The desired username for the new user.
  - `email` (string, required): The email address of the user.
  - `password` (string, required): The password for the new user.
- Response: Returns the newly created user details.

#### User Login

- URL: `/api/v1/accounts/login/`
- Method: POST
- Description: Logs in a user and generates an authentication token.
- Request Body:
  - `username` (string, required): The username of the user.
  - `password` (string, required): The password of the user.
- Response: Returns the user details and the authentication token.

#### User Logout

- URL: `/api/v1/accounts/logout/`
- Method: POST
- Description: Logs out the currently authenticated user.

### Tracker Endpoints

#### Get All Entries

- URL: `/api/v1/tracker/entries/`
- Method: GET
- Description: Retrieves all entries for the currently authenticated user.
- Response: Returns a list of entries.

#### Create Entry

- URL: `/api/v1/tracker/entries/`
- Method: POST
- Description: Creates a new entry for the currently authenticated user.
- Request Body:
  - `date` (string, optional): The date of the entry (format: YYYY-MM-DD).
  - `time` (string, optional): The time of the entry (format: HH:MM).
  - `text` (string, required): The text description of the entry.
  - `calories` (integer, optional): The calorie value for the entry.
- Response: Returns the newly created entry.

#### Get Entry Details

- URL: `/api/v1/tracker/entries/<int:pk>/`
- Method: GET
- Description: Retrieves the details of a specific entry.
- Response: Returns the entry details.

### Controls Endpoints

#### Get User Profile

- URL: `/api/v1/profile/`
- Method: GET
- Description: Retrieves the details of the currently authenticated user profile.

#### Get All Entries

- URL: `/api/v1/tracker/entries/all/`
- Method: GET
- Description: Retrieves all entries for all users (accessible only to users with the "admin" or "user_manager" role).
- Response: Returns a list of entries.

#### Get All Users

- URL: `/api/v1/users/all/`
- Method: GET
- Description: Retrieves all users (accessible only to users with the "admin" or "user_manager" role).
- Response: Returns a list of users.

#### Get User Details

- URL: `/api/v1/users/<int:pk>/`
- Method: GET
- Description: Retrieves the details of a specific user (accessible only to users with the "admin" or "user_manager" role).
- Response: Returns the user details.

#### Update User Details

- URL: `/api/v1/users/<int:pk>/`
- Method: PUT
- Description: Updates the details of a specific user (accessible only to users with the "admin" or "user_manager" role).
- Request Body: Same as the Register User endpoint.
- Response: Returns the updated user details.

#### Delete User

- URL: `/api/v1/users/<int:pk>/`
- Method: DELETE

- Description: Deletes a specific user (accessible only to users with the "admin" or "user_manager" role).

#### Filter Entries by Query and Date

- URL: `/api/v1/tracker/entries/all/?query=foodname&date=YYYY-MM-DD`
- Method: GET
- Description: Retrieves entries filtered by the specified query and date for all users. This endpoint is accessible only to users with the "admin" or "user_manager" role.
- Parameters:
  - `query`: The query string to filter entries by (e.g., "milk").
  - `date`: The specific date to filter entries by (e.g., "2023-06-19").
- Response: Returns a list of entries that match the specified query and date.

#### Get Users by Role

- URL: `/api/v1/users/all/?role=admin`
- Method: GET
- Description: Retrieves users filtered by the specified role. This endpoint is accessible only to users with the "admin" or "user_manager" role.
- Parameters:
  - `role`: The role to filter users by (e.g., "admin").
- Response: Returns a list of users that have the specified role.

Note: Replace `<int:pk>` with the corresponding entry ID or user ID, respectively. Pagination is given whenever required.
