import mysql.connector
from tkinter import *
import random

connection = mysql.connector.connect(
    user = 'root',
    database = 'example',
    password = 'brother112112!'
)

cursor =  connection.cursor()
loggedIn = False

def getDatabase():
    cursor.execute("SELECT * FROM account_table")
    db = cursor.fetchall()

    return db

#----------------------------------------HANDLES LOG-IN CHECKING----------------------------------------------
#Log-In checking is done similarly to a door lock, in that the multiple columns act like pins.
#If each pin is up (True), the door will unlock. If not, the log-in is invalid.

def login_fname_check(fname, database):
    isValid = False
    i = 0
    while i<len(database) and isValid == False:
        if fname == database[i][0]:
            isValid = True
        else:
            isValid = False
            i += 1

    return isValid

def login_lname_check(lname, database):
    isValid = False
    i = 0
    while i<len(database) and isValid == False:
        if lname == database[i][1]:
            isValid = True
        else:
            isValid = False
            i += 1

    return isValid

def login_pin_check(pin, database):
    isValid = False
    i = 0
    while i<len(database) and isValid == False:
        if pin == int(database[i][2]):
            isValid = True
        else:
            isValid = False
            i += 1

    return isValid

def login_AC_check(ac, database):
    isValid = False
    i = 0
    while i<len(database) and isValid == False:
        if ac == int(database[i][3]):
            isValid = True
        else:
            isValid = False
            i += 1

    return isValid

def login_master_check(namef, namel, accountnumber, pin):
    db = getDatabase()

    fname_check = login_fname_check(namef, db)
    lname_check = login_lname_check(namel, db)
    ac_check = login_AC_check(accountnumber, db)
    pin_check = login_pin_check(pin, db)

    #print(fname_check)
    #print(lname_check)
    #print(ac_check)
    #print(pin_check)

    if(fname_check == True and lname_check == True and ac_check == True and pin_check == True):
        return True
    else:
        return False
    
#----------------------------------------HANDLES LOG-IN CHECKING----------------------------------------------
def findAccount(fname, lname):
    db = getDatabase()

#----------------------------------------HANDLES MONEY FUNCTIONS----------------------------------------------
def getBalance(fname, lname, pin, ac):
    cursor.execute("SELECT balance FROM account_table WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s", (fname, lname, pin, ac) )
    db = cursor.fetchall()
    #print(db)

    return db

def deposit(amount, fname, lname, pin, ac):
    startingbal = getBalance(fname, lname, pin, ac)
    
    alterData = "UPDATE account_table SET balance = %s + %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
    values = (startingbal[0][0], amount, fname, lname, pin, ac,)
    cursor.execute(alterData, values)
    connection.commit()

def withdraw(amount, fname, lname, pin, ac):
    startingbal = getBalance(fname, lname, pin, ac)
    
    alterData = "UPDATE account_table SET balance = %s - %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
    values = (startingbal[0][0], amount, fname, lname, pin, ac,)
    cursor.execute(alterData, values)
    connection.commit()

def transfer(amount, fname, lname, tfname, tlname, pin, ac, tac, tpin):
    startingbal = getBalance(fname, lname, pin, ac)
    startingbaltransfer = getBalance(tfname, tlname, tpin, tac)
    
    alterData = "UPDATE account_table SET balance = %s - %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
    alterData2 = "UPDATE account_table SET balance = %s + %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
    values = (startingbal[0][0], amount, tfname, tlname, pin, ac,)
    values2 = (startingbaltransfer[0][0], amount, tfname, tlname, tpin, tac,)
    cursor.execute(alterData, values)
    cursor.execute(alterData2, values2)
    connection.commit()

#----------------------------------------HANDLES MONEY FUNCTIONS----------------------------------------------
#----------------------------------------HANDLES ACCOUNT MODIFICATION----------------------------------------------
def modify(choice, fname, lname, pin, ac):
    if choice == "1":
        changefname = input("What is your first name?")
        changelname = input("What is your last name?")

        alterData = "UPDATE account_table SET first_name = %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
        values = (changefname, fname, lname, pin, ac)
        alterData2 = "UPDATE account_table SET last_name = %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
        values2 = (changelname, fname, lname, pin, ac)
        cursor.execute(alterData, values)
        cursor.execute(alterData2, values2)
        connection.commit()
    elif choice == "2":
        changepin = input("What is your new pin?")

        alterData = "UPDATE account_table SET pin = %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
        values = (changepin, fname, lname, pin, ac)
        cursor.execute(alterData, values)
        connection.commit()
    elif choice == "3":
        changeac = input("What is your new account number?")

        alterData = "UPDATE account_table SET accountnumber = %s WHERE first_name = %s and last_name = %s and pin = %s and accountnumber = %s"
        values = (changeac, fname, lname, pin, ac)
        cursor.execute(alterData, values)
        connection.commit()
#----------------------------------------HANDLES ACCOUNT MODIFICATION----------------------------------------------
# Opens new account
def open_account(fname, lname, pin, balance):
    accountnumber = random.randint(1000000, 9999999)
    addData = "INSERT INTO account_table (first_name, last_name, accountnumber, pin, balance, admin) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (fname, lname, accountnumber, pin, balance, 1)
    cursor.execute(addData, values)
    connection.commit()

def login(fname, lname, ac):
    print(f"Welcome, {fname} {lname}")

    while loggedIn == True:
        choice = input("Do you want to:\n1. Deposit money\n2. Withdraw money\n3. Transfer money\n4. Edit account details\n5. Log Out\n")
        print(choice)

        if choice == "1":
            deposit_amount = float(input("How much do you want to deposit?"))
            pinNumber = int(input("What is your PIN? "))
            deposit(deposit_amount, fname, lname, pinNumber, ac)
        elif choice == "2":
            withdraw_amount = float(input("How much do you want to withdraw?"))
            pinNumber = int(input("What is your PIN? "))
            withdraw(withdraw_amount, fname, lname, pinNumber, ac)
        elif choice == "3":
            transferfname = input("First name of who would you like to transfer to")
            transferlname = input("Last name of who would you like to transfer to")
            transfer_amount = float(input("How much do you want to transfer?"))
            transfer_ac = int(input("What is the recepients account number?"))
            transfer_pin = int(input("What is the recepients pin number?"))
            pinNumber = int(input("What is your PIN? "))
            transfer(transfer_amount, fname, lname, transferfname, transferlname, pinNumber, ac, transfer_ac, transfer_pin)
        elif choice == "4":
            choice2 = input("Would you like to: \n1. Change first and last name\n2. Change pin number\n3. Change account number")
            pinNumber = int(input("What is your PIN? "))
            modify(choice2, fname, lname, pinNumber, ac)
        elif choice == "5":
            loggedIn == False
            quit()

        else:
            print("Choose a valid response.")
    
while loggedIn == False:
    choice = input("Do you want to:\n1. Open new account\n2. Login to existing account\n3. Exit program\n")
    print(choice)

    if choice == "1":
        userFName = input("What is your first name? ")
        userLName = input("What is your last name? ")
        pinNumber = int(input("What is your PIN? "))
        startBalance = float(input("How much money do you want to deposit? "))
        open_account(userFName, userLName, pinNumber, startBalance)
        loggedIn = TRUE
        login(userFName, userLName)
    elif choice == "2":
        userFName = input("Enter your first name: ")
        userLName = input("Enter your last name: ")
        pinNumber = int(input("Enter your pin: "))
        accountNumber = int(input("Enter your account number: "))
        loggedIn = TRUE
        

        if login_master_check(userFName, userLName, accountNumber,pinNumber) == True:
            login(userFName, userLName, accountNumber)
            
        else:
            print("These credentials do not match our records.")
    elif choice == "3":
        print("Exiting program...")
        quit()
    else:
        ("Choose a valid response.")
    

















for item in cursor:
    print(item)






cursor.close()
connection.close()

