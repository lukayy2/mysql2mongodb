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

## Configuration
 - Copy the ``config.example.ini`` File to ``config.ini``
 - Change the Variables to your needs

## Usage
```
pip install -r requirements.txt
python3 mysql2mongodb.py
```