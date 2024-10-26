import requests
import pandas as pd
import time
from datetime import datetime

# 使用 Fugle API 範例取得台灣股市即時資料
API_KEY = "YOUR_FUGLE_API_KEY"  # 替換為你的 Fugle API Key
BASE_URL = "https://api.fugle.tw/realtime/v0.3/intraday/quote"

# 要觀察的股票清單（股票代碼）
stock_symbols = ["2330", "0050", "2610"]  # 台積電、元大台灣50、華航

# 設定你的購買成本價格
cost_price = {
    "2330": 600.0,
    "0050": 120.0,
    "2610": 20.0
}

# Function: 取得即時股價資料
def get_stock_data(stock_id):
    response = requests.get(
        f"{BASE_URL}?symbolId={stock_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["data"]["info"]["name"],
            "current_price": data["data"]["quote"]["trade"]["price"]
        }
    else:
        print(f"Failed to get data for {stock_id}, status code: {response.status_code}")
        return None

# Function: 計算損益百分比
def calculate_profit_percentage(current_price, cost_price):
    return ((current_price - cost_price) / cost_price) * 100

# Main loop to check stock data and print results
def main():
    while True:
        # 取得所有股票的即時資料
        results = []
        for symbol in stock_symbols:
            stock_data = get_stock_data(symbol)
            if stock_data:
                current_price = stock_data["current_price"]
                cost = cost_price[symbol]
                profit_percentage = calculate_profit_percentage(current_price, cost)
                results.append([stock_data["name"], current_price, cost, profit_percentage])
        
        # 顯示資料
        df = pd.DataFrame(results, columns=["股票名稱", "現價", "成本價", "損益百分比"])
        print("\n\n" + str(datetime.now()))
        print(df)
        
        # 每隔 60 秒更新一次資料
        time.sleep(60)

if __name__ == "__main__":
    main()
