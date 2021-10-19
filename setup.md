#### setup

##### python

1. Create a virtual environment (optional)
2. run "python -m pip install requirements.txt" in cmd

##### mysql

1. setup a mysql server
2. run `setup.sql` in mysql
3. create a user with access to 'INSERT', 'UPDATE', 'DELETE', 'SELECT'
4. write the correct information into connector on sql_functions.py

##### a few accounts for testing

1. run setup.py
2. run `INSERT INTO Administrators (userID) VALUES (1);` in mysql