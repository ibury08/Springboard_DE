import pytest
import argparse
from banking_system import Account, SavingsAccount, CheckingAccount, Customer, withdraw, deposit


def test_account():
    acc = Account(1, 1, 100)
    with pytest.raises(ValueError):
        acc.withdraw('d')
    with pytest.raises(ValueError):
        acc.withdraw(-10)
    acc.withdraw(20)
    assert acc.balance == 80
    with pytest.raises(ValueError):
        acc.withdraw(100)
    with pytest.raises(ValueError):
        acc.deposit('string')
    with pytest.raises(ValueError):
        acc.deposit(-100)
    acc.deposit(100)
    assert acc.balance == 180


def test_savings():
    sa = SavingsAccount(1, 1, 1000, 1000)
    with pytest.raises(ValueError):
        sa.withdraw(100)


def test_checking():
    ca = CheckingAccount(1, 1, 100)
    ca.withdraw(101)
    assert ca.balance == -6
