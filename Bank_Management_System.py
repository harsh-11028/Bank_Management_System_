# banking_system.py

# Abstract Base Class
class Account:
    def __init__(self, account_number, account_holder_id, initial_balance=0.0):
        self._account_number = account_number
        self._account_holder_id = account_holder_id
        self._balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposit successful. Current Balance: ₹{self._balance}")
            return True
        else:
            print("Invalid deposit amount.")
            return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Withdrawal successful. Current Balance: ₹{self._balance}")
            return True
        else:
            print("Insufficient funds or invalid amount.")
            return False

    def display_details(self):
        return f"Account No: {self._account_number}, Balance: ₹{self._balance}"

    def get_account_number(self):
        return self._account_number

    def get_holder_id(self):
        return self._account_holder_id

    def get_balance(self):
        return self._balance

class SavingsAccount(Account):
    def __init__(self, account_number, account_holder_id, initial_balance=0.0, interest_rate=0.01):
        super().__init__(account_number, account_holder_id, initial_balance)
        self._interest_rate = interest_rate

    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        print(f"Interest applied. New Balance: ₹{self._balance}")

    def display_details(self):
        return super().display_details() + f", Interest Rate: {self._interest_rate * 100}%"

class CheckingAccount(Account):
    def __init__(self, account_number, account_holder_id, initial_balance=0.0, overdraft_limit=0.0):
        super().__init__(account_number, account_holder_id, initial_balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self._balance + self._overdraft_limit:
            self._balance -= amount
            print(f"Withdrawal successful. Current Balance: ₹{self._balance}")
            return True
        else:
            print("Overdraft limit exceeded or invalid amount.")
            return False

    def display_details(self):
        return super().display_details() + f", Overdraft Limit: ₹{self._overdraft_limit}"

class Customer:
    def __init__(self, customer_id, name, address):
        self._customer_id = customer_id
        self._name = name
        self._address = address
        self._accounts = []

    def add_account(self, account_number):
        if account_number not in self._accounts:
            self._accounts.append(account_number)

    def get_id(self):
        return self._customer_id

    def display_details(self):
        return f"Customer ID: {self._customer_id}, Name: {self._name}, Address: {self._address}, Accounts: {self._accounts}"

    def get_accounts(self):
        return self._accounts

class Bank:
    def __init__(self):
        self._customers = {}
        self._accounts = {}
        self._admin_password = "admin123"

    def create_customer_and_account(self):
        customer_id = input("Enter Customer ID: ")
        if customer_id in self._customers:
            print("Customer already exists. Cannot proceed.")
            return

        name = input("Enter Name: ")
        address = input("Enter Address: ")
        acc_number = input("Enter unique Account Number: ")

        if acc_number in self._accounts:
            print("Account already exists with this number.")
            return

        acc_type = input("Enter account type (savings/checking): ")
        balance = float(input("Enter initial balance: "))

        if acc_type == "savings":
            acc = SavingsAccount(acc_number, customer_id, balance)
        elif acc_type == "checking":
            overdraft = float(input("Enter overdraft limit: "))
            acc = CheckingAccount(acc_number, customer_id, balance, overdraft)
        else:
            print("Invalid account type.")
            return

        self._customers[customer_id] = Customer(customer_id, name, address)
        self._accounts[acc_number] = acc
        self._customers[customer_id].add_account(acc_number)
        print("Customer and Account created successfully.")

    def show_all_customers(self):
        pw = input("Enter admin password: ")
        if pw == self._admin_password:
            for cust in self._customers.values():
                print(cust.display_details())
        else:
            print("Access Denied: Not Admin.")

    def show_all_accounts(self):
        pw = input("Enter admin password: ")
        if pw == self._admin_password:
            for acc in self._accounts.values():
                print(acc.display_details())
        else:
            print("Access Denied: Not Admin.")

    def deposit(self):
        acc_num = input("Enter Account Number: ")
        amount = float(input("Enter amount to deposit: "))
        if acc_num in self._accounts:
            self._accounts[acc_num].deposit(amount)
        else:
            print("Account not found.")

    def withdraw(self):
        acc_num = input("Enter Account Number: ")
        amount = float(input("Enter amount to withdraw: "))
        if acc_num in self._accounts:
            self._accounts[acc_num].withdraw(amount)
        else:
            print("Account not found.")

    def transfer(self):
        from_acc = input("Enter FROM Account: ")
        to_acc = input("Enter TO Account: ")
        amount = float(input("Enter amount to transfer: "))
        if from_acc in self._accounts and to_acc in self._accounts:
            if self._accounts[from_acc].withdraw(amount):
                self._accounts[to_acc].deposit(amount)
        else:
            print("One or both account numbers not found.")

    def apply_interest_to_all(self):
        for acc in self._accounts.values():
            if isinstance(acc, SavingsAccount):
                acc.apply_interest()

def main():
    bank = Bank()
    while True:
        print("\n--- BANK MENU ---")
        print("1. Create Customer and Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Funds")
        print("5. Show All Customers")
        print("6. Show All Accounts")
        print("7. Apply Interest to Savings Accounts")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            bank.create_customer_and_account()
        elif choice == '2':
            bank.deposit()
        elif choice == '3':
            bank.withdraw()
        elif choice == '4':
            bank.transfer()
        elif choice == '5':
            bank.show_all_customers()
        elif choice == '6':
            bank.show_all_accounts()
        elif choice == '7':
            bank.apply_interest_to_all()
        elif choice == '8':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
