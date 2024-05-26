import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

app = Flask(__name__)

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Function to fetch stock data


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    return hist

# Function to plot stock data


def plot_stock_data(hist, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'])
    plt.title(f'Stock Closing Prices for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    plt.tight_layout()
    image_filename = f'{ticker}_plot.png'  # Just the filename
    image_path = os.path.join('static', image_filename)
    plt.savefig(image_path)
    plt.close()
    return image_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    ticker = request.form['ticker']
    hist = fetch_stock_data(ticker)
    image_path = plot_stock_data(hist, ticker)
    return redirect(url_for('result', image=image_path))


@app.route('/result')
def result():
    # Extract just the filename from the query parameter, no 'static/' prefix
    image = request.args.get('image')
    if image.startswith('static/'):  # Just a safety check
        image = image[7:]  # Strip 'static/' from the start
    return render_template('result.html', image=image)


if __name__ == '__main__':
    app.run(debug=True)
