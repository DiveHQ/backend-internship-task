## 1. Following instruction are given for Unix/MacOs , for windows refer here:https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
## Installing Pip
```bash
python3 -m pip install --user --upgrade pip
```
## Setting up virtual environment
# Install venv
```bash
python3 -m pip install --user virtualenv
```
# Creating virtual environment
```bash
python3 -m venv <venv name>
```
# Activate & Deactivate virtual environment
```bash
source <venv_name>/bin/activate
source <venv_name>/bin/deactivate
```
## Installing Dependencies
# Inside virtual environment
```bash
pip install flask python-dotenv requests flask-jwt-extended validators os
```

## 2. To run the test suite
```bash
python -m unittest src/test_calorie.py
```
## 3. To run the api server
```bash
export FLASK_ENV=development
export FLASK_APP=src
export FLASK_DEBUG=1
flask run
```
