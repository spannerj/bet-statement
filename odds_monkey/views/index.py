from flask import flash, Blueprint, render_template, redirect, url_for, request
import json
from odds_monkey.views.queries import getstatement, getpayments, getopeningbalance, getuser, getplayers
import calendar
from flask_login import login_user, logout_user, login_required
import flask_login
import requests

# This is the blueprint object that gets registered into the app in blueprints.py.
index = Blueprint('index', __name__)


@index.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = getuser(request.form['username'])
        if (user is None) or (request.form['password'] != user.password):
            error = 'Invalid Login. Please try again.'
        else:
            login_user(user)
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index.user_page'))
    return render_template('login.html', error=error)


@index.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.login'))


class Month:

    def __init__(self, year, month, profit):
        self.year = year
        self.month = month
        self.profit = profit


@index.route("/scores", methods=['GET'])
def scores():
    url = 'https://fantasyfootball.telegraph.co.uk/premier-league/json/fixtures/all'
    response = requests.get(url)
    fixtures_dict = {}
    fixtures_dict = response.json()
    players = getplayers()

    players_json = json.loads(players)

    latest_week = 42
    for fixture in fixtures_dict:
        if fixture['RESULT'] == 'X':
            if int(fixture['WEEK']) < latest_week:
                latest_week = int(fixture['WEEK'])
    max_week = latest_week - 1
 
    return render_template('players.html', players=players_json, max_week=max_week)


@index.route("/statement", methods=['GET'])
@login_required
def user_page():
    data = getstatement()
    user = flask_login.current_user
    payments = getpayments(user.page_route)
    opening_balance = getopeningbalance(user.page_route)
    results = build_user_results(user.page_route, json.loads(data))
    totals = calculate_totals(payments, opening_balance, results)

    return render_template('page.html', **locals())


def calculate_totals(payments, opening_balance, results):
    totals = {}
    profit = 0
    paid = 0
    for result in results:
        profit = profit + float(result.profit.replace(',', ''))

    profit = profit + float(opening_balance)

    for payment in payments:
        paid = paid + payment.amount

    totals['Total Profit'] = format_number(profit)
    totals['Total Paid'] = format_number(paid)
    totals['Money Owed'] = format_number(profit - float(paid))

    return totals


def build_user_results(user, statement):
    results = []
    year_list = []

    # extract years
    for years in statement:
        for year, month_list in years.items():
            year_list.append(year)

    # reverse sort years so newest listed first
    year_list.sort(reverse=True)

    # for each year
    for year in year_list:
        cnt = 0
        for months in years[year]:
            # loop through and store months in reverse order
            for i in range(12, 0, -1):
                if str(i) in months:
                    if user in months[str(i)]:
                        if cnt > 0:
                            year = ''
                        record = Month(year, calendar.month_name[i], format_number(months[str(i)][user]))
                        results.append(record)
                        cnt += 1

    return results


def format_number(amount):
    return '{0:,.2f}'.format(amount)
