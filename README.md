# datareach_web
Django DataReach API 

# Setup
1. Clone repo
2. Install conda 4.4+, python 3+, brew (latest versions should be fine. Python actually not really needed since conda with provision that for you I think as below)
3. Install and start postgresql:
```
brew update
brew install postgresql
brew services start postgresql
```
4. Create a database with a name you want or use default configurations (which will create database with the same name as your system username) with command below:
```
createdb
```
5. Enter database shell and create a new user:
```
# <db_name> is the name of the db you created in step 4
psql -s <db_name>

# create user (where <username> and <password> are desired username and password respectively) and grant permissions
create user <username> password '<password>';
GRANT ALL PRIVILEGES ON DATABASE db_name TO <username>;

# quit
\q
```
6. Setup all dependencies within the included environment with:
```
$ conda env create -f environment.yml
```
7. Activate the environment. As the instructions after setting up the environment should say, you can activate or deactivate the environment with:
```
# activate
source activate datareachdev

# deactivate
source deactivate
```
8. open datareach_web/settings.py and modify accordingly:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name, # <-- should be the name of the database you created (if using defaults, your username)
	'USER': '<username>', # <-- username as in step 5
	'PASSWORD': '<password>', # <-- password as in step 5
	'HOST': 'localhost',
	'PORT': '',
    }
}
```
9. make migrations file and migrate:
```
# create tables for api
python manage.py makemigrations api
python manage.py migrate api

# create tables for authentication tokens
python manage.py migrate authtoken
python manage.py migrate
```
10. make django superuser (with this you can access admin panel and authenticate yourself)
```
# follow prompts
python manage.py createsuperuser
```
# Usage
Start the server and start making requests to localhost port 8000:
```
python manage.py runserver
```

# API Schema
```
# You can actually test out the API by using the browser to first (IMPORTANT!) log into /admin so the token is stored in the
# browser and then directly navigating to api/ to use the provided interface.
#
# If using postman, please read below:
# NOTE: To access /api, you must first authenticate first by POST to /auth with username and password fields of the superuser 
# you created above, or other users you create later. The POST request will return an authentication token, which you must use # in the header following standard token authentication practices, where <token> is the returned token:
# key: Authorization
# value: Token <token>
# NOTE: All POST requests must end in backslash
# NOTE: Requests bodies for GET or POST can be form-data, x-www-form-urlencoded, raw
# NOTE: You may navigate to /admin to fill the db with some data (login using superuser credentials), or use the API.

# get list of hospitals (if superuser), or get information of your own hospital (if normal user)
GET api/hospitals/

# create new hospital
POST api/hospitals/
{
  "name":<desired_name>
}
# ALL FIELDS REQUIRED

# get any specific hospital (if superuser), or get your own hospital information, if supplying your own hospital id (otherwise get rejected)
GET api/hospitals/id/

# get list of doctors (if superuser), or get your own information (if normal user)
GET api/doctors/
# get any specific doctor (if superuser), or get your own information, if supplying your own id (otherwise get rejectd)
GET api/doctors/id/
# PUT and DELETE still need to be properly implemented

# create new user (doctor)
POST api/doctors/
{
  "username":<desired_username>,
  "password":<desired_password>,
  "first_name":<desired_first_name>,
  "last_name":<desired_last_name>,
  "hospital_group":<desired_hospital_affiliation>
}
# NOTE: hospital_group is the GROUP name that the desired hospital maps to
# ALL FIELDS REQUIRED

# get list of patients (if superuser), or get patients of your hospital (if normal user)
GET api/patients/

# create new patient 
POST api/patients/
{
  check models.py, and note hospital field should be id of desired Hospital, NOT the id of the group of the hospital
}
# ALL FIELDS REQUIRED

# get any specific patient (if superuser), or get patient of your hospital (if normal user) or rejected if not your patient
GET api/patients/id/

# perform standard actions on any specific patient (if superuser), or your own hospital's patients only and get rejected otherwise (if normal user)
PUT/DELETE api/patients/id/

# get list of visits (if superuser), or get visits of your hospital (if normal user)
GET api/visits/

# create new visit
POST api/visits/
{
  check models.py, and note the patient field should be id of associated patient
}

# get any specific visit (if superuser) or get visit of your hospital if providing correct id or get rejected otherwise
GET api/visits/id/

# perform standard actions on any specific visit (if superuser), or your own hospital's visit if providing correct id or get rejected otherwise
PUT/DELETE api/visits/id/
```

