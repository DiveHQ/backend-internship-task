# CalorieTrack

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About <a name = "about"></a>
This is a REST API for tracking daily calorie intake 

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

### Prerequisites (Without Docker)
* Python (3.9 and above)

### Prerequisites (With Docker)
* Python (3.9 and above)
* Docker

### Installing

### Step 1: Activate virtual environment and install packages

#### 1.1 Create python virtual environment
```
python3 -m venv venv
```
#### 1.2.1 Activate python virtual environment
- On MacOS
```
source /venv/bin/activate
```
- On Windows
```
source ~/{project_path}/venv/Scrpt
```

#### 1.4 Install poetry
```
pip install poetry 
```

#### 1.3 Install python packages
```
poetry install
```

### Step 2: Configure Environment Variables
Make a copy of `.env.example`. This newly created file should be `.env`
```
cp .env.example .env
```
#### 2.1 Fill out environment variables
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

### Step 3: Running CalorieTrack locally

#### Without Docker
- Ensure the virtual environment is activated. If not see step 1.2
- Ensure that all dependencies are installed. If not see steps 
- Ensure environment variables are filled with the correct details
- Start CalorieTrack server with using the code snippet below
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