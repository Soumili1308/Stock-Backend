import gspread, yfinance as yf, time
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("1laE4mKAj2KondZapRRJWPF6tRY1eIz9fukGBp36g5gU").sheet2

stocks = ["AAPL", "GOOGL", "MSFT"]  # Add more as needed

def update_sheet():
    while True:
        data = []
        for stock in stocks:
            ticker = yf.Ticker(stock)
            hist = ticker.history(period="1d", interval="1m")
            last = hist.tail(1)
            if not last.empty:
                row = [
                    stock,
                    str(last.index[-1]),
                    float(last['Open']),
                    float(last['High']),
                    float(last['Low']),
                    float(last['Close']),
                    float(last['Volume']),
                ]
                data.append(row)
        sheet.clear()
        sheet.append_row(["Stock", "Timestamp", "Open", "High", "Low", "Close", "Volume"])
        for row in data:
            sheet.append_row(row)
        time.sleep(10)