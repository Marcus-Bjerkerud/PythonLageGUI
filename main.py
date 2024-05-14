import sqlite3
import csv
from tkinter import *
from tkinter import messagebox

# Create a database connection
conn = sqlite3.connect('kundeDatabase.db')

# Create a cursor
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS customers (
            customer_number integer,
            name text,
            email text,
            phone_number integer,
            postal_code integer,
            city text
            )""")

# Commit changes
conn.commit()

# Load postal codes and cities from CSV
postal_codes = {}
with open('postnummer.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    for row in reader:
        if len(row) >= 2:
            postal_codes[row[0]] = row[1]

# Load customers from CSV
def load_customers_from_csv():
    with open('kunder.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 6:
                customer_number, name, email, phone_number, postal_code, city = row
                c.execute("INSERT INTO customers VALUES (:customer_number, :name, :email, :phone_number, :postal_code, :city)",
                          {
                              'customer_number': customer_number,
                              'name': name,
                              'email': email,
                              'phone_number': phone_number,
                              'postal_code': postal_code,
                              'city': city
                          })
        conn.commit()

load_customers_from_csv()

# Define functions for database handling
def add_customer():
    if postal_code.get() in postal_codes and postal_codes[postal_code.get()] == city.get():
        conn = sqlite3.connect('kundeDatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO customers VALUES (:customer_number, :name, :email, :phone_number, :postal_code, :city)",
                  {
                      'customer_number': customer_number.get(),
                      'name': name.get(),
                      'email': email.get(),
                      'phone_number': phone_number.get(),
                      'postal_code': postal_code.get(),
                      'city': city.get()
                  })
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Error", "Invalid postal code or city")

def delete_customer():
    conn = sqlite3.connect('kundeDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE customer_number=?", (delete_box.get(),))
    if c.fetchone() is not None:
        c.execute("DELETE from customers WHERE customer_number=?", (delete_box.get(),))
        messagebox.showinfo("Success", "Customer deleted successfully")
    else:
        messagebox.showerror("Error", "No such customer found")
    delete_box.delete(0, END)
    conn.commit()
    conn.close()

def query():
    conn = sqlite3.connect('kundeDatabase.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM customers WHERE customer_number=? OR name=? OR email=? OR phone_number=?", 
              (search_box.get(), search_box.get(), search_box.get(), search_box.get()))
    records = c.fetchall()
    if records:
        print_records = ''
        for record in records:
            print_records += str(record) + "\n"
        query_label = Label(root, text=print_records)
        query_label.grid(row=12, column=0, columnspan=2)
    else:
        messagebox.showerror("Error", "No such customer found")
    conn.commit()
    conn.close()

# Create GUI with Tkinter
root = Tk()
root.title('Customer Database')

# Create Text Boxes
customer_number = Entry(root, width=30)
customer_number.grid(row=0, column=1, padx=20)
name = Entry(root, width=30)
name.grid(row=1, column=1)
email = Entry(root, width=30)
email.grid(row=2, column=1)
phone_number = Entry(root, width=30)
phone_number.grid(row=3, column=1)
postal_code = Entry(root, width=30)
postal_code.grid(row=4, column=1)
city = Entry(root, width=30)
city.grid(row=5, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

search_box = Entry(root, width=30)
search_box.grid(row=11, column=1, pady=5)

# Create Text Box Labels
customer_number_label = Label(root, text="Customer Number")
customer_number_label.grid(row=0, column=0)
name_label = Label(root, text="Name")
name_label.grid(row=1, column=0)
email_label = Label(root, text="Email")
email_label.grid(row=2, column=0)
phone_number_label = Label(root, text="Phone Number")
phone_number_label.grid(row=3, column=0)
postal_code_label = Label(root, text="Postal Code")
postal_code_label.grid(row=4, column=0)
city_label = Label(root, text="City")
city_label.grid(row=5, column=0)

delete_box_label = Label(root, text="Delete Customer Number")
delete_box_label.grid(row=9, column=0)

search_box_label = Label(root, text="Search Customer")
search_box_label.grid(row=11, column=0)

# Create Submit Button
submit_btn = Button(root, text="Add Customer to Database", command=add_customer)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a Delete Button
delete_btn = Button(root, text="Delete Customer", command=delete_customer)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Create a Query Button
query_btn = Button(root, text="Search Customer", command=query)
query_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

root.mainloop()