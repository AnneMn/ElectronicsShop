import sqlite3
class MyData(object):

    def __init__(self):
        pass
    '''
    def insert_customer (self, cust_id, cust_name):
    def insert_onlineCustomer (self, cust_id, email, card_info):
    def insert_contractCustomer (self, cust_id, account_no, date_of_billing):
    def insert_product (self, prod_id, prod_price, man_name, prod_type):
    def insert_warehouse (self, ware_name, prod_id, prod_quantity):
    def insert_store (self, store_name, region, prod_id, prod_quantity):
    def insert_manufacturer (self, man_name, prod_id, prod_quantity):
    def insert_deliveryCompany (self, cust_id, tracking_no, date_of_delivery):
    def insert_sales (self, prod_id, unit_sales, total_price):
    def bought_by(self, cust_id, prod_id, prod_quantity, unit_price, total_price, store_name, date_of_purchase):
    def delivered_by(self, tracking_no, date_of_actual_delivery):
    def reorder_from(self, man_id, prod_id, prod_quantity, reorder_status):
    '''

    def find_package(self, tracking_no):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        self.tracking_no = tracking_no
        myCursor.execute('SELECT cust_id FROM deliverycompany WHERE tracking_no =?',(tracking_no,))
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def find_customerinfo(self, cust_id):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        self.cust_id = cust_id
        myCursor.execute('SELECT email FROM onlinecustomers WHERE cust_id=?',(cust_id,))
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def find_content(self, tracking_no):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        self.tracking_no = tracking_no
        myCursor.execute('SELECT content FROM deliverycompany WHERE tracking_no =?',(tracking_no,))
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def highest_customer(self):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute('SELECT cust_id,cust_name,MAX(total_amount_spent) FROM customers')
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def toptwo_byprice(self):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute('SELECT total_price FROM Sales ORDER BY total_price DESC LIMIT 2')
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)
    
    def toptwo_byunitsales(self):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute('SELECT unit_sales FROM Sales ORDER BY unit_sales DESC LIMIT 2')
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def out_of_stock(self, store):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute("SELECT pName FROM stores WHERE region = 'Nairobi' AND stock = 0")
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)
    
    def late_delivery(self):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute('SELECT tracking_no FROM deliveredBy WHERE date_of_actual_delivery NOT IN (SELECT date_of_delivery FROM deliverycompany)')
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)

    def get_invoice(self, cust_id):
        myConnection = sqlite3.connect('project.db')
        myCursor = myConnection.cursor()
        myCursor.execute('SELECT * FROM boughtBy WHERE cust_id = ?', (cust_id,))
        myRS = myCursor.fetchall()
        myConnection.commit()
        myConnection.close()
        print(myRS)


myDb = MyData()
'''
myDb.find_package('TN1234')
myDb.find_customerinfo('O1J5D')
myDb.find_content('TN1234')
myDb.highest_customer()
myDb.toptwo_byprice()
myDb.toptwo_byunitsales()
myDb.out_of_stock('store1_inventory')
myDb.late_delivery()
myDb.get_invoice('O1J5D')
'''
