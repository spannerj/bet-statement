from odds_monkey.models import Statement, Payment, User, Player
import json
from sqlalchemy.sql import desc


def getplayers():
    """Get Players."""
    results = Player.query.with_entities(Player.players).order_by(desc(Player.created_at)).limit(1).first()
    return json.dumps(results.players, separators=(',', ':'), sort_keys=False)


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
