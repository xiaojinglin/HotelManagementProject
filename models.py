import mysql.connector as mysql
from datetime import date


myhost = "localhost"
myuser = "python"
mypass = "pythonmysql"

db = mysql.connect(host=myhost,user=myuser,password=mypass,database="mydatabase")   
cur = db.cursor(buffered = True)
cur.execute("DROP TABLE IF EXISTS customers")
sql_create = ''' CREATE TABLE IF NOT EXISTS customers(
                                            id INT AUTO_INCREMENT PRIMARY KEY,
                                            first_name VARCHAR(255),
                                            last_name VARCHAR(255),
                                            phone CHAR(11)
                                            )'''
cur.execute(sql_create)

cur.execute("DROP TABLE IF EXISTS rooms")
sql_create = ''' CREATE TABLE IF NOT EXISTS rooms(
                                            id INT AUTO_INCREMENT PRIMARY KEY,
                                            room_no VARCHAR(50),
                                            customer_id INT,
                                            room_type CHAR(50),
                                            price INT,
                                            check_in DATE,
                                            check_out DATE
                                            )'''
cur.execute(sql_create)

class Customer:
    def __init__(self,id):
        self.id = id
        sql = 'SELECT * FROM customers WHERE id=%s'
        cur.execute(sql,(id,))
        self.customer = cur.fetchone()
        self.first_name = self.customer[1]
        self.last_name = self.customer[2]
        self.phone = self.customer[3]

    def __repr__(self):
        return f'First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}'

    @staticmethod
    def add(customer_info):
        sql = 'INSERT INTO customers(first_name,last_name,phone) VALUES(%s,%s,%s)'
        val = customer_info
        cur.execute(sql,val)
        db.commit()

    def get(self):
        return self.customer

    def update(self,fist_name,last_name,phone):
        sql = 'UPDATE customers SET first_name=%s,last_name=%s,phone=%s WHERE id=%s'
        val = (fist_name,last_name,phone,self.id)
        cur.execute(sql,val)
        db.commit()

    def delete(self):
        sql = 'DELETE FROM customers WHERE id=%s'
        val = (self.id,)
        cur.execute(sql,val)
        db.commit()

    @staticmethod
    def exist_customer(customer_info):
        sql = 'SELECT * FROM customers WHERE first_name=%s and last_name=%s and phone=%s'
        val = customer_info
        cur.execute(sql,val)
        return cur.fetchone()


class Room:
    def __init__(self,id):
        self.id = id
        sql = 'SELECT * FROM rooms WHERE id=%s'
        cur.execute(sql, (id,))
        room = cur.fetchone()
        self.room_no = room[1]
        self.customer_id = room[2]
        self.room_type = room[3]
        self.price = room[4]
        self.check_in = room[5]
        self.check_out = room[6]

    def __repr__(self):
        return f'''room NO: {self.room_no}, 
                \rcustomer id: {self.customer_id}, 
                \rroom type: {self.room_type},
                \rprice: {self.price},
                \rcheck_in: {self.check_in},
                \rcheck_out: {self.check_out}'''

    @staticmethod
    def add(room_no,room_type,price):
        sql = 'SELECT * FROM rooms WHERE room_no=%s'
        val = (room_no,)
        if cur.execute(sql,val)==None:
            sql = 'INSERT INTO rooms(room_no,room_type,price) VALUES(%s,%s,%s)'
            val = (room_no,room_type,price)
            cur.execute(sql,val)
            db.commit()

    @staticmethod
    def get_id(room_no):
        sql = 'SELECT id FROM rooms WHERE room_no=%s'
        val = (room_no,)
        cur.execute(sql,val)
        return cur.fetchone()[0]

    def update(self,customer_id,check_in,check_out):
        sql = 'UPDATE rooms SET customer_id=%s,check_in=%s,check_out=%s WHERE id=%s'
        val = (customer_id,check_in,check_out,self.id)
        cur.execute(sql,val)
        db.commit()

    @staticmethod
    def get_rooms(customer_id):
        sql = 'SELECT id,room_no,check_in,check_out FROM rooms WHERE (customer_id=%s and check_out>%s)'
        val = (customer_id,date.today())
        cur.execute(sql,val)
        return cur.fetchall()

    @staticmethod
    def get_room_nos(room_type):
        room_nos = []
        sql = 'SELECT room_no FROM rooms WHERE (room_type=%s and customer_id IS NULL)'
        val = (room_type,)
        cur.execute(sql,val)
        for room_no in cur.fetchall():
            room_nos.append(room_no[0])
        return room_nos


def initialize():
    for i in range(1,10):
        Room.add(f'10{i}','single',89)
        Room.add(f'20{i}','double',120)
    Customer.add(('John','Knight','5022222222'))
    sql = 'SELECT * FROM customers WHERE first_name=%s and last_name=%s and phone=%s'
    val = ('John','Knight','5022222222')
    cur.execute(sql,val)
    new_customer_id = cur.fetchone()[0]
    Room(1).update(new_customer_id,'2023-03-02','2023-03-10')