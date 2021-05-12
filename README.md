# task-mng-restapi
It is a backend restapi server for task management system. developed by using django, django-restframework, mysql

## steps to run the api server

1, Create databse or use existing data by dumping mql dump (you can get it from dump and API collection dir)
2, Change the necessary database setting in config_util.py under baseproject
3, Create a `python 3.7` and above virtual environment 
4, Activate and install the requirements using `pip install -r requirement.txt`
5, If fresh db, migrate the db tables to db using `python manage.py migrate`
6, Run django server using 'python manage.py runserver'


## check the API using postman

1, Open the postman and import the collection (you can get it from dump and API collection dir)
2, send the API and test it


