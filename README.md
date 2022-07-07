# Backend for PlayRoom App

### Local setup
Python 3.10+ required


Create & activate virtualenv
```bash
virtualenv venv
source venv/bin/activate
```

Install dependencies from `requirements.txt`
```bash
pip install -r requirements.txt
```


Setup your local Postgres database (create user with password, 
create database, grant permissions to db)

Create `.env` file
```
touch .env
```


Fill `.env` with your own credentials for db and app by the following example


```
POSTGRES_USER=<your_db_user>
POSTGRES_PASSWORD=<your_db_password>
host=<your_host>
port=5432
POSTGRES_DB=<your_db>
secret_key=<any_random_string>
algorithm=HS256
```


Fill db with tables
```bash
python -m scripts.setupdb
```


Create admin
```bash
 python -m scripts.create_admin -u <admin_username> -p <admin_password>
```


Run app
```bash
uvicorn main:app --reload
```


### Optional

If you want to drop db, run the following command
```bash
python -m scripts.dropdb
```
