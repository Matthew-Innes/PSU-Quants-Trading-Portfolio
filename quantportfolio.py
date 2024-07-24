import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib as plt
import mysql.connector as mysql
import random
from datetime import datetime
from pandas_datareader import data as pdr
from sqlaccess import get_connection as get_db_connection
from sqlaccess import get_connection as get_user
yf.pdr_override()

# Establishes connection with the database. Enter the details in sqlaccess.py.
mydb = get_db_connection()
mycursor = mydb.cursor()

class Portfolio:
  def __init__(self, name, cash):
    self.name = name
    self.cash = cash
    self.AUM = None
    self.portfolio_beta = None
    
    self.profit_loss = None
    self.sharpe_ratio = None
    self.total_return = None
    self.expense_ratio = None
    self.avg_price_to_earnings = None
  
  def sql_to_pd_dataframe(self, table):
    df = pd.read_sql('SELECT * FROM tradedb.{tbl}'.format(tbl = table), con = mydb)
    return df
  
  def generate_order_id():
    while True:
        order_id = random.randint(1000000000, 9999999999)
        if order_id not in existing_ids:
            existing_ids.add(order_id)
            return order_id
        else:
            raise ValueError("Duplicate order ID found!")

  

  def usd_to_cents(amount):
    cents = amount * 100
    return cents
  
  def calculate_overall_return(self):
    holdings_df = sql_to_pd_dataframe("holdings")
    holdings_df['pr_times_pl'] = holdings_df.position_ratio * holdings_df.profit_loss
    portfolio_return = (holdings_df['pr_times_pl'].sum()) / 100
    return portfolio_return

  # calculates assets under management
  def calculate_AUM(self):
    holdings_df = sql_to_pd_dataframe("holdings")
    holdings_df['cp_times_q'] = holdings_df.current_price * holdings_df.quantity
    self.AUM = (holdings_df['cp_times_q'].sum()) / 100
    return self.AUM

  def performance_vs_benchmark(self, start_date, end_date, benchmark):
    # portfolio_returns = self.calculate_return(self.get_portfolio_value(start_date), self.get_portfolio_value(end_date))
    # benchmark_returns = self.calculate_return(benchmark.get_value(start_date), benchmark.get_value(end_date))
    # performance_difference = portfolio_returns - benchmark_returns
    # return performance_differences

    # changes datetime64 to datetime.datetime format
    df['time'] = df['time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    portfolio_return = self.calculate_overall_return()
    benchmark_return = self.calculate_benchmark_return(start_date, end_date, benchmark)
    outperformance = portfolio_return - benchmark_return
    return outperformance

  
  def calculate_benchmark_return(self, start_date, end_date, benchmark):
     benchmark_df = self.sql_to_pd_dataframe(benchmark)

        # Filter benchmark data within the specified date range
     benchmark_df = benchmark_df[(benchmark_df['date'] >= start_date) & (benchmark_df['date'] <= end_date)]

        # Calculate benchmark return based on your specific data structure and calculations
        # Here are a couple of possible approaches:

        # Approach 1: Single return value
        # Assuming your benchmark data contains a 'return' column representing daily returns
     benchmark_return = benchmark_df['return'].sum()

        # Approach 2: Compound returns
        # Assuming your benchmark data contains a 'return' column representing daily returns
        # benchmark_return = (1 + benchmark_df['return']).prod() - 1

     return benchmark_return

  def find_us_stock_trade(self, ticker, id):
    return None

  # specify the format of this method so that the SQL query works properly
  # buys/sells US stock
  def place_US_stock_order(self, ticker, price, order_type, quantity):
    total_cost = price * quantity  # convert to cents later

    if order_type == "B":
      if total_cost > self.cash:
        print("Not enough funds")
        print("Order Cost: ${cost}, Balance: ${cash}".format(cost = total_cost, cash = self.cash))

      else:
        # don't forget to store the purchase price in cents on MySQL for floating point precision
        self.cash -= total_cost
        mycursor.execute("INSERT INTO tradedb.trades (order_id, user_id, order_type, ticker, price, {quantity})\
                          VALUES (0000000001, 'minnes', 'B', 'TSLA', 80000, 5);".format(quantity = quantity))

    if order_type == "S":
      # do the sell thing
    
    else:
      # raise an error/exception, print error for now
      print("Order type can be either 'B' (buy) or 'S' (sell)")


  def calculate_sharpe_ratio(self, risk_free_rate): 
    # utilize total return, total volatility, and risk free rate
    # updates sharpe ratio attribute
    return None

  def portfolio_report(self):
    print("Portfolio Name: {name}".format(name = self.name))
    print("Portfolio AUM: ${aum}".format(aum = self.AUM))
    print("\nPortfolio Statistics:")
    print("Portfolio Return: {total_return}%".format(total_return = self.total_return))
    print("Portfolio Beta: {beta}".format(beta = self.portfolio_beta))
    print("Portfolio Profit-Loss: ${profit_loss}".format(profit_loss = self.profit_loss))
    print("Portfolio Sharpe Ratio: {sharpe_ratio}".format(sharpe_ratio = self.sharpe_ratio))
    print("Portfolio Expense Ratio: {expense_ratio}".format(expense_ratio = self.expense_ratio))
    print("Portfolio Average P/E: {avg_price_to_earnings}".format(avg_price_to_earnings= self.avg_price_to_earnings))
    #etc.

  # calculates the weight of the portfolio's securities
  def positions_weight(self):
    return None

  def graph_us_stocks_holdings(self):
    # utilize matplotlib to graph
    return None