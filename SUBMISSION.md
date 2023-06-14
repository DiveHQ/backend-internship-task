# CalorieTrack

## Table of Contents
+ [Getting Started](#getting_started)
+ [Prerequisites](#prerequisites)
+ [Activating Virtual Environments](#virtual_environment)
+ [Configuring Environment Variables](#environment_variables)
+ [Running app](#running_app)


## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites <a name = "prerequisites"></a>

### Prerequisites (Without Docker)
* Python (3.9 and above)

### Prerequisites (With Docker)
* Python (3.9 and above)
* Docker

### Step 1: Activate virtual environment and install packages <a name = "virtual_environment"></a>

#### 1.1 Create python virtual environment
```
python3 -m venv venv
```
#### 1.2.1 Activate python virtual environment
- On MacOS
```
source venv/bin/activate
```
- On Windows
```
source venv/Scripts/activate
```

#### 1.4 Install poetry
```
pip install poetry 
```

#### 1.3 Install python packages
```
poetry install
```

### Step 2: Configure Environment Variables <a name = "environment_variables"></a>
Make a copy of `.env.example`. This newly created file should be `.env`
```
cp .env.example .env
```
#### 2.1 Fill out environment variables
Ensure to fill out the environment variables. The admin user is created automatically when the application starts so the details should be filled before starting the app.

```
SECRET=Used for encoding and decoding JWT
NUTRIXION_APP_ID=The application ID obtained from nutrixionix
NUTRIXION_APP_KEY=The application key obtained from nutritionix
API_URL=The url for the calories API provider
ADMIN_EMAIL=The email for the admin
ADMIN_FIRST_NAME=The first name for the admin
ADMIN_LAST_NAME=The last name for the admin
PASSWORD=The admin's password
PASSWORD_CONFIRMATION=The admin's password confirmation
```

### Step 3: Running CalorieTrack locally <a name = "running_app"></a>

#### Without Docker
- Ensure the virtual environment is activated. If not see step 1
- Ensure that all dependencies are installed. If not see step 1
- Ensure environment variables are filled with the correct details
- Start CalorieTrack server using the code snippet below
```
uvicorn src.main:app --reload
```

#### With Docker
- Ensure Docker daemon is running
- Start CalorieTrack server with using the code snippet below
```
docker-compose up -d
```

#### With make installed
Run
```
make start
```
#### Without make
Run
```
docker-compose up -d
```
Then start CalorieTrack server using the code snippet below
```
uvicorn src.main:app --reload
```

####