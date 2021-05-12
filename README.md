# task-mng-restapi
It is a backend restapi server for task management system. developed by using django, django-restframework, mysql

## steps to run the api server

1, Create databse or use existing data by dumping mql dump (you can get it from dump and API collection dir)  <br />
2, Change the necessary database setting in config_util.py under baseproject  <br />
3, Create a `python 3.7` and above virtual environment  <br />
4, Activate and install the requirements using `pip install -r requirement.txt`  <br />
5, If fresh db, migrate the db tables to db using `python manage.py migrate`  <br />
6, Run django server using `python manage.py runserver`  <br />


## check the API using postman

1, Open the postman and import the collection (you can get it from dump and API collection dir)  <br />
2, Send the API and test it


