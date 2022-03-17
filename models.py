from select import select
import mysql.connector as mysql
import datetime


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
        return f'first name: {self.first_name}, last name: {self.last_name}, phone: {self.phone}'

    @staticmethod
    def add(first_name,last_name,phone):
        sql = 'SELECT * FROM customers WHERE first_name=%s and last_name=%s and phone=%s'
        val = (first_name,last_name,phone)
        if cur.execute(sql,val)==None:
            sql = 'INSERT INTO customers(first_name,last_name,phone) VALUES(%s,%s,%s)'
            val = (first_name,last_name,phone)
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

    def update(self,customer_id,check_in,check_out):
        sql = 'UPDATE rooms SET customer_id=%s,check_in=%s,check_out=%s WHERE id=%s'
        val = (customer_id,check_in,check_out,self.id)
        cur.execute(sql,val)
        db.commit()

if __name__ == '__main__':
    for i in range(1,10):
        Room.add(f'10{i}','single',89)
        Room.add(f'20{i}','double',12)
    Customer.add('John','Knight','5022222222')
    sql = 'SELECT * FROM customers WHERE first_name=%s and last_name=%s and phone=%s'
    val = ('John','Knight','5022222222')
    cur.execute(sql,val)
    new_customer_id = cur.fetchone()[0]
    Room(1).update(new_customer_id,'2022-03-02','2022-03-10')

