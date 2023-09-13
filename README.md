# Mysql 2 MongoDB (Server-to-Server Copy)

## What does it do?
Converts a Table from a Mysql Server into an MongoDB Collection.

Steps:
 - Connects to both Servers (Mysql and MongoDB)
 - Reads Table-Details
 - Uses Table-Details to create the Collection with Validator (required Fields and Datatypes)
 - Reads Rows in Bulk from Mysql Table
 - Inserts Documents in Bulk to MongoDB Collection

## Requirements
 - Python 3
 - pip installed 

## Configuration (using named arguments)
The following CLI-Arguments are available
 ```
-h, --help            show this help message and exit
--mysqlHost MYSQLHOST
                    Mysql(Source) Hostname or IP
--mysqlUser MYSQLUSER
                    Mysql(Source) Usernmae
--mysqlPassword MYSQLPASSWORD
                    Mysql(Source) Password
--mysqlDatabase MYSQLDATABASE
                    Mysql(Source) Database
--mysqlTable MYSQLTABLE
                    Mysql(Source) Table
--mongoHost MONGOHOST
                    MongoDB(Dest) Hostname or IP
--mongoUser MONGOUSER
                    MongoDB(Dest) Username
--mongoPassword MONGOPASSWORD
                    MongoDB(Dest) Password
--mongoDatabase MONGODATABASE
                    MongoDB(Dest) Database
--mongoCollection MONGOCOLLECTION
                    MongoDB(Dest) Collection
--selectlimit SELECTLIMIT
                    Rows to select at once (Tweak for best Performance) Default: 100

 ```

## Configuration (using config.ini File)
 - Copy the ``config.example.ini`` File to ``config.ini``
 - Change the Variables to your needs

## Usage
```
pip install -r requirements.txt
python3 mysql2mongodb.py # using config.ini File
# < OR >
python3 mysql2mongodb.py --mysqlHost 127.0.0.1 --mysqlUser user --mysqlPassword pw --mysqlDatabase test --mysqlTable table --mongoHost 127.0.0.1 --mongoUser user --mongoPassword pw --mongoDatabase test --mongoCollection collection
```