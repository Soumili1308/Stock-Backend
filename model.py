import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)

def predict_stock(stock_name):
    # Open the stock-specific sheet
    sheet = client.open(f"{stock_name}_StockData").sheet2  # Each stock should have its own Sheet
    data = sheet.get_all_records()
    
    if not data:
        return ("no data", 0)

    df = pd.DataFrame(data)
    
    # Prepare features and target
    if 'Target' not in df.columns:
        return ("no target", 0)
    
    X = df.drop(columns=["Target"])
    y = df["Target"]

    if X.empty or y.empty:
        return ("insufficient data", 0)

    clf = RandomForestClassifier()
    clf.fit(X, y)

    # Predict based on the latest available data
    latest_features = X.iloc[-1]
    prediction = clf.predict([latest_features])[0]
    confidence = max(clf.predict_proba([latest_features])[0]) * 100

    return ("rise" if prediction == 1 else "fall",confidence)