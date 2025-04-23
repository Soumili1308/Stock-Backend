from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from model import train_lstm, predict_next

app = Flask(_name_)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    stock_data = pd.read_csv("https://docs.google.com/spreadsheets/d/1laE4mKAj2KondZapRRJWPF6tRY1eIz9fukGBp36g5gU/export?format=csv")
    predictions = {}

    for stock in stock_data['Stock'].unique():
        df = stock_data[stock_data['Stock'] == stock]
        if len(df) > 60:
            close_prices = df[['Close']].values.astype(float)
            model, scaler = train_lstm(close_prices)
            pred = predict_next(model, scaler, close_prices)
            predictions[stock] = float(pred)

    return jsonify(predictions)

if _name_ == '_main_':
    app.run(debug=True)