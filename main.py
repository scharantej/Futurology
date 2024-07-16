
from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']

    # Get historical stock data
    data = yf.download(ticker, period='5y')
    data['Date'] = data.index
    data['Close'] = data['Close'].round(2)

    # Split data into training and testing sets
    train_data = data[:-252]
    test_data = data[-252:]

    # Create and train linear regression model
    model = LinearRegression()
    model.fit(train_data[['Date']], train_data[['Close']])

    # Predict future stock prices
    predictions = model.predict(test_data[['Date']])

    # Create plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test_data['Date'], y=test_data['Close'], name='Actual'))
    fig.add_trace(go.Scatter(x=test_data['Date'], y=predictions, name='Predicted'))
    fig.update_layout(title='Stock Price Forecast', xaxis_title='Date', yaxis_title='Price')

    # Save plotly graph as html
    graph_div = fig.to_html()

    # Render forecast template with plotly graph
    return render_template('forecast.html', graph_div=graph_div)

if __name__ == '__main__':
    app.run(debug=True)
