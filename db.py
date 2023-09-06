import mysql.connector
from utils.status import status
import os
from dotenv import load_dotenv


# Define class items
class Item:
    table_name = "items"
    def __init__(self, name, part_number):
        self.name = name
        self.part_number = part_number

class Resistor(Item):
    table_name = "resistors"
    def __init__(self, name, part_number, resistance, measurement):
        super().__init__(name, part_number)
        self.resistance = resistance
        self.measurement = measurement

class Computer(Item):
    table_name = "computers"
    def __init__(self, name, part_number, cpu, ram, storage):
        super().__init__(name, part_number)
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

class LED(Item):
    table_name = "leds"
    def __init__(self, name, part_number, color, brightness):
        super().__init__(name, part_number)
        self.color = color
        self.brightness = brightness

class Keyboard(Item):
    table_name = "keyboards"
    def __init__(self, name, part_number, numkeys, size, kbtype):
        super().__init__(name, part_number)
        self.numkeys = numkeys
        self.size = size
        self.kbtype = kbtype

# Function to connect to the MariaDB database
def connect_to_database():
    load_dotenv()
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


# Function to create the tables if they don't exist
def create_tables_if_not_exist():
    connection = connect_to_database()
    cursor = connection.cursor()

    # Get a list of all the defined classes in the current module
    classes = [cls for cls in globals().values() if isinstance(cls, type) and issubclass(cls, Item)]

    for cls in classes:
        if hasattr(cls, 'table_name'):
            table_name = cls.table_name  # Use the class's table_name attribute as the table name
            init_method = cls.__init__  # Get the __init__ method of the class
            init_params = list(init_method.__code__.co_varnames[1:])  # Extract parameter names, excluding 'self'

            # Generate the SQL table creation statement dynamically
            columns = [f"{name} VARCHAR(255)" for name in init_params]
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join(columns)})"
            print(status.INFO, query, end='\r')
            cursor.execute(query)
            print(status.OK, query)

    connection.commit()
    connection.close()




# Function to insert an item into the database
def insert_item(item):
    connection = connect_to_database()
    cursor = connection.cursor()

    if not hasattr(item, 'table_name'):
        raise ValueError("The item class must have a 'table_name' attribute specifying the database table name.")

    table_name = item.table_name

    # Get the class attributes and their values
    attributes = vars(item)

    # Generate the query and values dynamically
    columns = ', '.join(attributes.keys())
    placeholders = ', '.join(['%s'] * len(attributes))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    values = tuple(attributes.values())
    print(status.INFO,f"INSERT INTO {table_name} ({columns}) VALUES {values}",end='\r')
    cursor.execute(query, values)
    connection.commit()
    connection.close()
    print(status.OK,f"INSERT INTO {table_name} ({columns}) VALUES {values}")



# Set items
keyboard = Keyboard("Steelseries Apex Pro", "1", "104", "100%", "Mechanical")
resistor = Resistor("Resistor 1", "R123", "10 Ohms", "High Precision")
computer = Computer("Computer 1", "C456", "Intel Core i7", "16 GB", "1 TB SSD")
led = LED("LED 1", "L789", "Red", "High Brightness")



#RUN
try:
    # Create the tables if they don't exist
    create_tables_if_not_exist()
    
    # Insert the items into the database
    insert_item(resistor)
    insert_item(computer)
    insert_item(led)
    insert_item(keyboard)

#catch any errors
except Exception as e:
    print('\n')
    print(status.ERROR,e)