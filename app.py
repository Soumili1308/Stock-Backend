from flask import Flask, render_template, request, jsonify
from model import predict_stock
import stock_fetcher

app = Flask(_name_)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    stock_name = request.json.get("stock")
    prediction, confidence = predict_stock(stock_name)
    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "message": f"The stock {stock_name} will likely {prediction}. Confidence: {confidence:.2f}%"
    })

if _name_ == "_main_":
    app.run(debug=True)