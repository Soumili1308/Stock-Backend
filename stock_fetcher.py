import time
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("StockData").sheet2

ts = TimeSeries(key='9SQ9ZB0S062D3QD9', output_format='pandas')

def update_sheet(stock):
    data, _ = ts.get_intraday(symbol=stock, interval='1min', outputsize='compact')
    df = data.tail(30)
    df['Target'] = (df['4. close'].diff().shift(-1) > 0).astype(int)
    df.to_csv(f"data/{stock}.csv")

    sheet.clear()
    sheet.append_row(df.columns.tolist())
    for row in df.values.tolist():
        sheet.append_row(row)

if _name_ == "_main_":
    while True:
        update_sheet("AAPL")
    time.sleep(20)