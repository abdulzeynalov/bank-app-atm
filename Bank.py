import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

username1 = 'abdulz'
password1 = hashlib.sha256("password".encode()).hexdigest()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, entered_username, entered_password):
        return self.username == entered_username and self.password == entered_password

class BankAccount:
    def __init__(self, user, initial_balance=0):
        self.user = user
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return amount
        else:
            return None

    def get_balance(self):
        return self.balance

new_username = input("Create a username: ")
new_password = input("Create a password: ")

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (new_username, new_password))
conn.commit()

user = User(new_username, new_password)
account = BankAccount(user, 100)

while True:
    entered_username = input("Enter your Username: ")
    entered_password = input("Enter your password: ")

    if user.login(entered_username, entered_password):
        print("Login successful.")
        while True:
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Logout")
            choice = input("Select an option (1/2/3/4): ")

            if choice == "1":
                amount_to_deposit = float(input("Enter the amount to deposit:"))
                if account.deposit(amount_to_deposit):
                    print("Deposit successful. New Balance:", account.get_balance())
                else:
                    print("Invalid deposit amount.")

            elif choice == "2":
                amount_to_withdraw = float(input("Enter the amount to withdraw: "))
                withdrawn_amount = account.withdraw(amount_to_withdraw)
                if withdrawn_amount is not None:
                    print(f"Withdrew ${withdrawn_amount}. New Balance:", account.get_balance())
                else:
                    print("Insufficient funds or invalid withdrawal amount.")

            elif choice == "3":
                print("Current balance:", account.get_balance())

            elif choice == "4":
                print("Logged out.")
                break

            else:
                print("Invalid choice. Please select a valid option")
    else:
        print("Invalid login credentials. Please try again")
