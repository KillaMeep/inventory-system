
# Inventory System

A simple Inventory management system using MariaDB for items lying around the house.


## DB Setup
1. Before anything else, make sure you have your DB set up.
2. For this code - as of right now -  It needs port 3306 open for tcp, and needs you to set the `port` value and `bind-address` in your `/etc/mysql/my.cnf` (or whevever your MariaDB config file is). Heres an example of what to change to open to all addresses on the local network (unsafe, but if its only in your network it should be fine.)

```
# Port or socket location where to connect
[client-server]
port = 3306

# Open to all addresses on local
[mysqld]
bind-address = 0.0.0.0
```
- This should mostly cover how to get the DB working. If you have any errors with this part, google is your friend.
## Using the `.env` File

This repository includes a `.env` file that contains sensitive configuration settings for logging into the DB. The `.env` file holds several items, heres how to set that up.

1. **Create a `.env` File:**

If a `.env` file doesn't already exist in the root directory of your project, create one.

2. **Edit the `.env` File:**

Open the `.env` file in a text editor of your choice and add or modify the necessary configuration variables. Heres the values that need modified.
```dotenv
DB_HOST=host-address
DB_USER=database-user-name
DB_PASSWORD=database-password
DB_DATABASE=database-name
```
- Now you should be set up! This works for all the files, so set it up once, and you can forget about it.
## Code Usage
1. You can define `Item` class which holds data ALL items in the system would have. Every class you create should have a variable set called `table.name`. This var will be used in generating the table name in the DB.
```python
class Item():
    table.name = 'items'
    def __init__(self,name,part_number)
        self.name = name
        self.part_number = part_number
```
2. You then can create subclasses which are for each item type, calling the `Item` class from earlier to use its name and part number vars!
```python
class Computer(Item):
    table_name = 'computers'
    # create the names for each value you want to make in __init__
    def __init__(self,name,part_number,cpu,ram,storage):
    # now we pull the vars from our Items class earlier
    super().__init__(name,part_number)
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
```
3. Awesome! Now that we have the `Item` class and the `Computer` subclass, we can send some data to the DB! Near the bottom of the `db.py` file, we have a comment (`#set items`). After this comment, we can add the new items we want to send to the db. For exmaple:
```python
#name, part number, cpu, ram, storage
computer = Computer("My Home PC", "computer123", "Intel Core i7", "16 GB", "1 TB SSD")

try:
    # leave this call, it looks at the classes from earlier, 
    # and will create the talbes in the DB.
    create_tables_if_not_exist()

    insert_item(computer) # and now we send our item into the DB!

except Exception as e: # add error logging
    print('\n')
    print(status.ERROR,e)

```
- This should mostly cover how to use this code, all you have to do now is run `db.py`! The `alldata.py` and `WIPEDB.py` files you just need to run. Keep in mind again, if you run the `WIPEDB.py` file, it WILL delete ALL of the data from your database!! This is highly dangerous, and I do not recommend it.
## Authors

- [@KillaMeep](https://www.github.com/KillaMeep)



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

