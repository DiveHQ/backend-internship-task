pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations users tracker
python3 manage.py migrate
