
from sqlalchemy import insert, update, select, create_engine, MetaData, Table, Column, String, Integer, Float, Boolean
import contextlib
import json
from hashlib import sha256
import sys
import argparse
import logging
import os
import re

# setup logging
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('dev.log')
fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

formatter = logging.Formatter(
    '%(asctime)s  %(name)s  %(levelname)s: %(message)s')
fileHandler.setFormatter(formatter)


@contextlib.contextmanager
def db_connect():
    connection = engine.connect()
    yield connection
    connection.close()


def insert_to_db(obj, table):
    """ Inserts a single instance of a class into the specified table.
    Args:
        - obj: instance of class to be inserted
        - table: (string) name of table to insert class instance
    Returns:
        - (int) Sets attribute id of instanct to the primary key of inserted row"""
    with db_connect() as db:
        try:
            results = db.execute(insert(table), vars(obj)).inserted_primary_key
        except Exception as e:
            logger.exception(str(e))
            raise
        obj.id = results[0]


def update_db(obj, table):
    """Updates a row in the specified table using the id attribute of the passed class instance argument as the primary key
    Args:
        - objs: instance of class to be updated
        - table: (string) name of table to update
    Returns:
        - Row count of updates rows. Returns 1 if successful."""
    with db_connect() as db:
        stmt = update(table).where(table.c.id == obj.id).values(vars(obj))
        results = db.execute(stmt)
    if results.rowcount > 0:
        logger.debug(f"Update successful, rows updated: {results.rowcount}")
    return results.rowcount


class Customer:
    """A class to represent a customer (also user).
    Attributes:
        - first_name: (string) first name of the customer
        - last_name: (string)  last name of the customer
        - address: (string)  mailing address of the customer
        - username: (string) username to access customer's accounts
        - password: (string) used with username to validate login
        - id: (int) the primary key of an instance stored in the database (set by insert_to_db)
        """

    def __init__(self, first_name, last_name, address, username, password, id=None):

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.username = username
        self.password = password
        self.id = id

    def __repr__(self):
        return f"Customer(first_name={self.first_name}, last_name={self.last_name}, address={self.address}, username={self.username}, password={self.password}, id={self.id})"


class Account:
    """A class to represent a bank account. Many-to-one relationship with class Customer.
    Attributes:
        - balance: (float) cash balance of the account
        - customer_id: (int) owner of the account; primary key (id attribute) of the Customer instance
        - account_type: (string) For this class and its subclasses, string representation of an instance's class name
    Methods:
        - deposit(self, amount): Takes one argument (amount) which is added to the existing balance.
        - withdraw(self, amount): Takes one argument (amount) which is subtracted from the existing balance.
        """

    def __init__(self, customer_id, id=None, balance=0):
        self.balance = balance
        self.customer_id = customer_id
        self.account_type = self.__class__.__name__
        self.id = id

    def __repr__(self):
        return f"Account(customer_id={self.customer_id}, id={self.id},balance={self.balance})"

    def deposit(self, amount):
        amount = validate_numeric(amount)
        self.balance += amount

    def withdraw(self, amount):
        amount = validate_numeric(amount)
        if self.balance >= amount:
            self.balance -= amount
            return f'Withdrawl of ${amount} successful, new balance is ${self.balance}'
        else:
            raise ValueError("Insufficient funds")


class SavingsAccount(Account):
    """A sub-class of Account, SavingsAccount also carries a minimum balance requirement.
    Attributes:
        - min_balance: Minimum balance for the account; cannot withdraw below this amount
    Methods:
        - withdraw(amount): Extends Account.withdraw() with minimum balance requirement
        - add_interest(n_periods): Computes interest for the account over n_periods.
        """

    def __init__(self, customer_id, id=None, balance=0.0, min_balance=1000.0):
        Account.__init__(self, customer_id, id, balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if self.balance - amount >= self.min_balance:
            Account.withdraw(self, amount)
        else:
            raise ValueError(
                f"Cannot withdraw below minimum balance of ${self.min_balance}")


class CheckingAccount(Account):
    """A sub-class of Account, CheckingAccount also charges a $5 overdraft fee for withdrawals that create a negative balance."""

    def __init__(self, customer_id, id=None, balance=0.0, overdraft_fee=5.0):
        Account.__init__(self, customer_id, id, balance)
        self.overdraft_fee = overdraft_fee

    def withdraw(self, amount):
        validate_numeric(amount)
        if self.balance - amount < 0:
            self.balance -= (amount + self.overdraft_fee)
            return f'Withdrawl of ${amount} successful, new balance is ${self.balance}'


def validate_numeric(input):
    """Helper function to check that user-input amounts for deposits and withdrawals are positive numerics
        Args: 
            input (str) - user input from command line
        Returns:
            input_asfloat - (float) converted input to float
    """
    try:
        input_asfloat = float(input)
        if input_asfloat <= 0:
            raise ValueError(f"Input cannot be negative. Got {input}")
    except:
        raise ValueError(f"Input must be numeric. Got: {input}")

    return input_asfloat


def return_logged_in(func):
    """Decorator used to return a user to the main menu after completion of the wrapped function
        Args:
            func (function) - function to wrap
        Returns:
            wrapper - wrapped func
    """
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return logged_in_main(active_user)
    return wrapper


def login():
    """Takes user input for credentials and checks against known users in the database. Stores successful login (e.g. Customer instance) as global active_user.
    """
    username = input("Username: ")
    pw = sha256(input("Password: ").encode()).hexdigest()
    logger.debug(f"Login attempt: user: {username}")
    with db_connect() as db:
        results = db.execute(select([customers]).where(
            customers.c.username == username)).fetchall()
    if len(results) > 0:
        global active_user
        active_user = Customer(results[0].first_name, results[0].last_name,
                               results[0].address, results[0].username, results[0].password, results[0].id)

        if active_user.password == pw:
            logger.info('Successful login')
            logger.debug(f'User login: {active_user.id}')
            logged_in_main(active_user)
        else:
            logger.debug(f"Failed login for user: {username}")
            logger.info("Incorrect Password")
            return main()
    else:
        logger.info("User does not exist")
        return main()


@return_logged_in
def create_account():
    """Takes user input choice and creates an instance of a subclass of Account (either SavingsAccount or CheckingAccount) based on input.
    Args:
        input() - must be a key of class_choices dict
    Returns:
        None - creates instance of either SavingsAccount or CheckingAccount, registers an intial deposit and inserts to db"""
    menu_str = "Which type of account would you like to create? \n\
        A - Savings account \n\
        B - Checking account \n\
        ? "
    class_choices = {'A': SavingsAccount, 'B': CheckingAccount}
    a = validate_choice(input(menu_str), class_choices)(
        customer_id=active_user.id)

    initial_deposit = input("Initial deposit amount? ")

    initial_deposit = validate_numeric(initial_deposit)

    if isinstance(a, SavingsAccount):
        if initial_deposit < a.min_balance:
            logger.info(
                f"Initial deposit must be greater than the minimum balance requirement of ${a.min_balance}.")
            return logged_in_main(active_user)
    a.balance = initial_deposit

    insert_to_db(a, accounts)
    if a.id:
        logger.info("Account created")
        logger.debug(f"New Account: {a}")


def create_customer():
    """Takes user inputs for Customer attributes, creates an instance of Customer, inserts Customer into database and returns to main menu
       Args:
       - input(): (str) input from command line for first_name, last_name, address, username, password
       Returns:
       - calls main() to return to main menu, after creating/inserting Customer into DB
    """
    pattern = re.compile('^[a-zA-Z]+$')
    first_name = input("First Name: ")
    while pattern.match(first_name) is None:
        logger.info('Name must contain only letters.')
        first_name = input("First Name: ")
    last_name = input("Last Name: ")
    while pattern.match(last_name) is None:
        logger.info('Name must contain only letters.')
        last_name = input("Last Name")
    address = input("Address: ")
    username = input("Username: ")
    password = sha256(input("Password: ").encode()).hexdigest()
    c = Customer(first_name, last_name, address, username, password)
    # check if customer already exists with that username
    with db_connect() as db:
        results = db.execute(select([customers]).where(
            customers.c.username == c.username)).fetchall()
    if len(results) > 0:
        logger.info('Username taken. Please choose a different username')
        create_customer()
    else:
        insert_to_db(c, customers)
        if c.id:
            logger.info('User successfully created.')
            logger.debug(f"New user: {c}")
    return main()


def logged_in_main(user):
    """Maps user input to dict of possible functions called via this menu
       Args:
           - user: (Customer) 
       Returns:
           - func: (function) called from dict of function options"""
    menu_str = f"Welcome {user.first_name}. \n\
        Account menu - Please select from the options below: \n\
        A - Check balance \n\
        B - Deposit \n\
        C - Withdraw \n\
        D - New Account \n\
        E - Logout \n\
            ? "

    account_funcs = {'A': return_logged_in(
        get_accounts), 'B': deposit, 'C': withdraw, 'D': create_account, 'E': logout}
    func = validate_choice(input(menu_str), account_funcs)
    return func()


def logout():
    """Deletes active_user, which is used to store a user id for a given session"""
    global active_user
    active_user = None
    logger.info("Logout successful. Goodbye.")


def get_accounts():
    """Queries database for all accounts with customer_id equal to logged in user. 
    Prints a table of accounts and balances.
    Returns a dict where key = Account ID and value = instance of Account class (or subclass)"""
    with db_connect() as db:
        results = db.execute(select([accounts]).where(
            accounts.c.customer_id == active_user.id)).fetchall()
        accts = {i[0]: getattr(sys.modules[__name__], i.account_type)(
            i.customer_id, i.id, i.balance) for i in results}
    for k, v in accts.items():
        print(
            f"Account ID: {k}   |   Account Balance: {v.balance}   |   Account Type: {v.account_type}")
    return accts


@return_logged_in
def deposit():
    """Deposits the specified amount into the account chosen by the user
        Args:
        input() - command line input from user
    Returns:
        None - calls Account.deposit()"""
    accts = get_accounts()
    menu_str = "Which account? "
    try:
        acct = accts[int(input(menu_str))]
    except:
        logger.info(f"Please enter a valid account number. Got: {input}")
        return logged_in_main(active_user)

    dep = input("How much to deposit? ")
    try:
        dep = validate_numeric(dep)
        acct.deposit(dep)
    except Exception as e:
        logger.info(str(e))
        return logged_in_main(active_user)
    rc = update_db(acct, accounts)
    if rc > 0:
        logger.info(f"Deposit successful, new balance: ${acct.balance}")


@return_logged_in
def withdraw():
    """Withdraws the specified amount from the account chosen by the user.
    Args:
        input() - command line input from user
    Returns:
        None - calls Account.withdraw()
    """
    accts = get_accounts()
    menu_str = "Which account?"
    try:
        acct = accts[int(input(menu_str))]
    except:
        logger.info(f"Please enter a valid account number. Got: {input}")
        return logged_in_main(active_user)

    w = input("How much to withdraw? ")

    try:
        w = validate_numeric(w)
        acct.withdraw(w)
    except Exception as e:
        logger.info(str(e))
        return logged_in_main(active_user)
    rc = update_db(acct, accounts)
    if rc > 0:
        logger.info(f"Withdrawal successful, new balance: ${acct.balance}")


def validate_choice(choice, func_dict):
    """Helper function to validate menu choices against dict of available options.
    Args:
    - choice: (str) User input, should be in func_dict.keys(). 
    - func_dict: (dict) Available options, keys should match expected user input, values are functions to execute upon choice. E.g. {'choiceA':funcA}
    Returns:
    - function returned by func_dict[key]"""
    try:
        func = func_dict[choice.upper()]
    except:
        #raise ValueError(f"Invalid Selection. Got: {choice}.")
        logger.info(f"Invalid Selction. Got: {choice}")
        if active_user is not None:
            logged_in_main(active_user)
        else:
            main()
    return func


def main(debug=False):
    """Initial menu that takes user input as key to dict to call functions as specified"""
    menu_str = "Welcome to Acme Banking System \n\
        Main menu - Please select from the options below: \n\
            A - Login \n\
            B - New User \n\
        ? "
    anon_funcs = {'A': login, 'B': create_customer}
    func = validate_choice(input(menu_str), anon_funcs)
    return func()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', help='Run in debug mode.', action='store_true')
    args = parser.parse_args()
    debug = args.debug

    active_user = None  # Instantiate a global variable to store in-session user
    if debug:
        logger.info('---Running in debug mode---')

        db_path = 'sqlite:///bankdata_debug.db'
    else:
        sys.tracebacklimit = 0
        db_path = 'sqlite:///bankdata.db'
    logger.debug(f'Database path: {db_path}')

    # Sqlite setup
    engine = create_engine(db_path)
    metadata = MetaData()
    customers = Table('customers', metadata, Column('id', Integer, primary_key=True), Column('first_name', String(255)), Column('last_name', String(
        255)), Column('address', String(255)), Column('username', String(255)), Column('password', String(255)), sqlite_autoincrement=True)
    accounts = Table('accounts', metadata, Column('id', Integer, primary_key=True), Column('account_type', String(255)), Column('customer_id', Integer),
                     Column('balance', Float), Column('min_balance', Float, default=0), Column('overdraft_fee', Float, default=0), sqlite_autoincrement=True)
    metadata.create_all(engine)
    main(debug)
