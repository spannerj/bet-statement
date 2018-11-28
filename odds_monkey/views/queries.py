from odds_monkey.models import Statement, Payment, User
import json


def getstatement():
    """Get Statement."""
    results = Statement.query.first()
    return json.dumps(results.statement, separators=(',', ':'), sort_keys=False)


def getopeningbalance(user):
    """Get Opening Balance."""
    result = Payment.query.filter(Payment.account == user, Payment.payment_date == None).first() # noqa
    if result is None:
        return 0
    else:
        return result.amount


def getpayments(user):
    """Get Payments."""
    return Payment.query.filter(Payment.account == user, Payment.payment_date != None) # noqa


def getuser(user):
    """"Get User"""
    return User.query.filter_by(username=user).first()
