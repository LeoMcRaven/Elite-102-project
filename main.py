import mysql.connector
from tkinter import *
import random

connection = mysql.connector.connect(
    user = 'root',
    database = 'example',
    password = 'brother112112!'
)

cursor =  connection.cursor()
loggedIn = FALSE

def open_account(fname, lname, pin, balance):
    accountnumber = random.randint(1000000, 9999999)
    addData = "INSERT INTO account_table (first_name, last_name, accountnumber, pin, balance, admin) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (fname, lname, accountnumber, pin, balance, 1)
    cursor.execute(addData, values)
    connection.commit()

def login_check(name, accountnumber, pin):
    nameCheck = FALSE
    pinCheck = FALSE
    numCheck = FALSE
    
    

    dbnames = cursor.execute("SELECT name FROM account_table")
    dbpins = cursor.execute("SELECT pin FROM account_table")
    dbaccountnumbers = cursor.execute("SELECT accountnumber FROM account_table")



    for names in dbnames:
        if names == name:
            nameCheck = TRUE
            break
    for pins in dbpins:
        if pins == pin:
            pinCheck = TRUE
            break
    for nums in dbaccountnumbers:
        if nums == accountnumber:
            numCheck = TRUE
            break
    
    if nameCheck == TRUE and pinCheck == TRUE and numCheck == TRUE:
        return TRUE
    else:
        return FALSE








while loggedIn == FALSE:
    choice = input("Do you want to:\n1. Open new account\n2. Login to existing account\n3. Exit program\n")
    print(choice)

    if choice == "1":
        first_name = input("What is your first name? ")
        last_name = input("What is your last name? ")
        pinNumber = int(input("What is your PIN? "))
        startBalance = float(input("How much money do you want to deposit? "))
        open_account(first_name, last_name, pinNumber, startBalance)
        loggedIn = TRUE
    elif choice == "2":
        userName = input("Enter your name: ")
        pinNumber = int(input("Enter your pin: "))
        accountNumber = int(input("Enter your account number: "))

        if(login_check(userName,accountNumber,pinNumber) == TRUE):
            print(f"Successfully logged in as: {userName}")
            loggedIn = TRUE
        else:
            print("Your credentials do not match our records.")
            loggedIn = FALSE

        
    elif choice == "3":
        print("Exiting program...")
        quit()
    else:
        ("Choose a valid response.")















for item in cursor:
    print(item)






cursor.close()
connection.close()

