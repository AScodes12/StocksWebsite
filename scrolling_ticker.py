import yfinance as yf
from flask import Flask, render_template_string
from stock_display import stock_display_bp

print("--> [1/4] Script started. Initializing Flask app...")
app = Flask(__name__)
app.register_blueprint(stock_display_bp)

# Define the stocks you want to track (Yahoo Finance symbols)
WATCHLIST = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOG", "META", "NFLX", "JPM"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sleek Live Stock Ticker</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-color: #0b0c0e;
            --text-main: #ffffff;
            --up-color: #00c805;
            --down-color: #ff3b30;
        }

        body {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            background-color: #0b0c0e;
            color: var(--text-main);
            overflow: hidden;
            padding: 16px 0;
            -webkit-font-smoothing: antialiased;
        }

        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background-color: transparent;
            box-sizing: border-box;
            padding: 20px 0;
            display: flex;
            align-items: center;
            border-top: 1px solid rgba(255,255,255,0.06);
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .ticker {
            display: flex;
            white-space: nowrap;
            padding-left: 100%;
            animation: ticker 240s linear infinite;
        }

        .ticker__item {
            display: inline-flex;
            align-items: center;
            padding: 0 26px;
            font-size: 16px;
            font-weight: 500;
            letter-spacing: 0.02em;
            border-left: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.2s ease, background-color 0.2s ease;
            text-decoration: none;
            color: inherit;
        }

        .ticker__item:first-child {
            border-left: none;
        }

        .ticker__item:hover {
            transform: scale(1.02);
            background-color: rgba(255,255,255,0.02);
        }

        .ticker__symbol {
            font-weight: 700;
            color: var(--text-main);
            margin-right: 10px;
        }

        .ticker__price {
            font-weight: 600;
            margin-right: 8px;
            color: #e7eaf6;
        }

        .ticker__session {
            font-size: 11px;
            color: #8f95a1;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-right: 10px;
        }

        .ticker__change {
            font-size: 16px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .up-trend { color: var(--up-color); }
        .down-trend { color: var(--down-color); }

        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }
    </style>
    
    <meta http-equiv="refresh" content="60">
</head>
<body>

    <div class="ticker-wrap">
        <div class="ticker">
            {% for stock in stocks %}
            <a class="ticker__item" href="/stock/{{ stock.symbol }}">
                <span class="ticker__symbol">{{ stock.symbol }}</span>
                <span class="ticker__price">${{ "%.2f"|format(stock.price) }}</span>
                <span class="ticker__session">{{ stock.session_label }}</span>
                <span class="ticker__change {% if stock.is_positive %}up-trend{% else %}down-trend{% endif %}">
                    <span>{% if stock.is_positive %}▲{% else %}▼{% endif %}</span>
                    <span>{% if stock.is_positive %}+{% endif %}{{ "%.2f"|format(stock.change_percent) }}%</span>
                </span>
            </a>
            {% endfor %}
        </div>
    </div>

</body>
</html>
"""

print("--> [2/4] Registering routes...")
@app.route('/')
def home():
    print("--> [ROUTE TRIGERRED] Fetching live stock data...")
    stock_data_list = []
    
    tickers = yf.Tickers(' '.join(WATCHLIST))
    
    for symbol in WATCHLIST:
        try:
            ticker = tickers.tickers[symbol]
            info = ticker.info
            regular_price = info.get("regularMarketPrice") or info.get("previousClose")
            prev_close = info.get("regularMarketPreviousClose") or info.get("previousClose")
            after_hours_price = info.get("postMarketPrice") or info.get("preMarketPrice")
            after_hours_change = info.get("postMarketChangePercent") or info.get("preMarketChangePercent")
            session_label = "Regular"

            if after_hours_price is not None:
                current_price = after_hours_price
                change_percent = after_hours_change if after_hours_change is not None else 0.0
                session_label = "After Hours"
            else:
                current_price = regular_price
                change_percent = info.get("regularMarketChangePercent")
                if change_percent is None and prev_close:
                    change_percent = ((current_price - prev_close) / prev_close) * 100

            if current_price is None:
                current_price = 0.0
            if change_percent is None:
                change_percent = 0.0

            stock_data_list.append({
                "symbol": symbol,
                "price": current_price,
                "change_percent": change_percent,
                "is_positive": change_percent >= 0,
                "session_label": session_label
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            
    tripled_data = stock_data_list * 3
    print(f"--> [ROUTE SUCCESS] Loaded data for {len(stock_data_list)} stocks.")
    return render_template_string(HTML_TEMPLATE, stocks=tripled_data)

print("--> [3/4] Verifying entry execution check...")
if __name__ == '__main__':
    print("--> [4/4] Main check passed! Launching Flask web server now...")
    app.run(debug=True, port=8080)
