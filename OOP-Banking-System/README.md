# Setup
`git clone git@github.com:ibury08/Springboard_DE.git`  
`cd Springboard_DE/OOP-Banking-System`  
`make init && make test`  (or `pip install -r requirements.txt && python -m pytest tests/`)

# Starting the app
`make run`  (or `python banking_system.py`) 

Or in debug mode for full stacktrace and dev database using `make debug` (or `python banking_system.py --debug`)
# Background
This project simulates a simple banking system via the command line, with the data being stored in sqlite database.
There are two primary classes - Customers and Accounts. A user must create or use an existing Customer instance in order to then access Accounts. The cl provides multiple options across interfaces to create new Accounts and update the attributes of existing accounts. The exhaustive list of user actions is:
1. Login
2. Create user
3. Check balance (of all accounts)
4. Deposit (increases balance by x)
5. Withdraw (decreases balance by x)
6. New Account (creates new SavingsAccount or CheckingAccount)
7. Logout (ends session)

A user may interact with two Account types - SavingsAccount and CheckingAccount. A SavingsAccount has a minimum balance requirement, preventing withdrawals that would leave an end balance below this amounts. A CheckingAccount can withdraw below a zero balance, though it is then charged an overdraft fee.


<div>
<img src="https://github.com/ibury08/Springboard_DE/blob/main/OOP-Banking-System/UML%20diagram.png"></img></div>

