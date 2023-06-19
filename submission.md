# Calorie Tracker Application

## Description
The Calorie Tracker is a web application that allows users to track their daily calorie intake by creating and managing entries.

## Setup
1. Clone the repository: 
    git clone https://github.com/MaheswaranPalaniselvan/nutritionix_api_fast_api.git
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
