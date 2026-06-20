import yfinance as yf
from flask import Blueprint, render_template_string, abort

stock_display_bp = Blueprint("stock_display", __name__)

DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ stock.name }} — Stock Detail</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
            background: #060b14;
            color: #edf2ff;
            min-height: 100vh;
            padding: 24px;
            -webkit-font-smoothing: antialiased;
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 22px;
        }
        .header__title {
            margin: 0;
            font-size: 32px;
            font-weight: 700;
        }
        .header__subtitle {
            margin: 6px 0 0;
            color: #90a3c4;
            font-size: 14px;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 14px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-radius: 999px;
            background: rgba(74, 217, 161, 0.12);
            color: #c8ffe4;
        }
        .company-badge {
            width: 72px;
            height: 72px;
            border-radius: 22px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            color: #e8ffef;
            font-size: 20px;
            font-weight: 700;
            margin-right: 18px;
        }
        .company-logo {
            width: 72px;
            height: 72px;
            border-radius: 22px;
            object-fit: contain;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 12px;
            margin-right: 18px;
        }
        .insight-panel {
            background: rgba(11, 19, 33, 0.94);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .insight-title {
            margin: 0 0 14px;
            color: #eef4ff;
            font-size: 18px;
            font-weight: 700;
        }
        .insight-list {
            display: grid;
            gap: 14px;
        }
        .insight-item {
            background: rgba(16, 26, 44, 0.92);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px;
            color: #eef4ff;
            font-size: 14px;
            line-height: 1.7;
        }
        .insight-item strong {
            display: block;
            margin-bottom: 8px;
            color: #c4d7ff;
        }
        @media (max-width: 1040px) {
            .grid-3 {
                grid-template-columns: repeat(2, minmax(140px, 1fr));
            }
            .stats {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 720px) {
            .grid-3 {
                grid-template-columns: 1fr;
            }
        }
        .hero-panel {
            background: #0f172b;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 28px;
            margin-bottom: 24px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 26px;
            align-items: center;
        }
        .hero-price {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .hero-price__value {
            font-size: 54px;
            font-weight: 800;
            letter-spacing: -0.05em;
            color: #ffffff;
        }
        .hero-price__change {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 18px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            color: #ffffff;
            font-size: 15px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
        }
        .hero-price__change.up-trend {
            background: rgba(74,217,161,0.18);
            color: #b8ffdc;
        }
        .hero-price__change.down-trend {
            background: rgba(255,59,48,0.18);
            color: #ffbeb7;
        }
        .hero-metrics {
            display: grid;
            gap: 12px;
        }
        .metric-pill {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 999px;
            padding: 12px 16px;
            color: #d9e6fc;
            font-size: 13px;
        }
        .overview-card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }
        .stat {
            padding: 18px 20px;
            border-radius: 18px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.18s ease, border-color 0.18s ease;
        }
        .stat:hover {
            transform: translateY(-2px);
            border-color: rgba(74,217,161,0.24);
        }
        .stat__label {
            display: block;
            font-size: 11px;
            color: #90a3c4;
            margin-bottom: 8px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .stat__value {
            font-size: 18px;
            font-weight: 700;
            color: #f7faff;
        }
        .stat__small {
            color: #a8b4d1;
            font-size: 13px;
            margin-top: 4px;
        }
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #8f95a1;
            text-decoration: none;
            font-size: 14px;
            margin-bottom: 18px;
        }
        .back-link:hover {
            color: #ffffff;
        }
        .small-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
        }
        .small-row span {
            color: #91a7c5;
            font-size: 13px;
        }
        .details-panel {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 18px 20px;
            margin-bottom: 24px;
            color: #e8efff;
        }
        .details-panel summary {
            font-weight: 700;
            cursor: pointer;
            list-style: none;
            margin-bottom: 14px;
        }
        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }
        .details-panel summary::-webkit-details-marker {
            display: none;
        }
        .details-panel summary::before {
            content: "Show more data";
            display: inline-block;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            color: #f8fbff;
        }
        .summary-card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .summary-title {
            margin: 0 0 14px;
            color: #8ea9c9;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }
        .summary-text {
            margin: 0;
            color: #e7ecf7;
            line-height: 1.75;
            font-size: 15px;
            max-height: 260px;
            overflow-y: auto;
            white-space: pre-wrap;
            padding-right: 6px;
        }
        .chart-card {
            background: linear-gradient(180deg, rgba(13, 22, 37, 0.98), rgba(9, 14, 25, 0.98));
            border: 1px solid rgba(74, 217, 161, 0.16);
            border-radius: 24px;
            padding: 26px;
            margin-bottom: 30px;
            box-shadow: 0 28px 58px rgba(0,0,0,0.24);
        }
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            margin-bottom: 18px;
        }
        .chart-header h2 {
            margin: 0;
            font-size: 18px;
            font-weight: 700;
        }
        .chart-header span {
            color: #8f95a1;
            font-size: 14px;
        }
        .chart-legend {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-top: 12px;
        }
        .chart-legend span {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #c1c6db;
        }
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 100%;
            display: inline-block;
        }
        .chart-wrapper {
            position: relative;
            width: 100%;
            min-height: 360px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a class="back-link" href="/">← Back to ticker</a>
        <div class="header">
            <div style="display:flex; align-items:center; gap:16px;">
                <span class="company-badge">{{ stock.symbol }}</span>
                <div>
                    <h1 class="header__title">{{ stock.name }} ({{ stock.symbol }})</h1>
                    <p class="header__subtitle">{{ stock.exchange }} · {{ stock.sector or 'Sector unknown' }}</p>
                </div>
            </div>
            <span class="badge">{{ stock.session_label }}</span>
        </div>

        <div class="hero-panel">
            <div class="hero-price">
                <div class="hero-price__value">{{ stock.formatted_price }}</div>
                <div class="hero-price__change {{ 'up-trend' if stock.is_positive else 'down-trend' }}">
                    <span>{% if stock.is_positive %}▲{% else %}▼{% endif %}</span>
                    <span>{{ stock.formatted_change }}</span>
                    <span>· {{ stock.currency }}</span>
                </div>
            </div>
            <div class="hero-metrics">
                <div class="metric-pill">Market Cap: {{ stock.formatted_market_cap }}</div>
                <div class="metric-pill">PE Ratio: {{ stock.formatted_pe_ratio }}</div>
                <div class="metric-pill">Volume: {{ stock.formatted_volume }}</div>
                <div class="metric-pill">Avg volume: {{ stock.formatted_avg_volume }}</div>
                <div class="metric-pill">Rating: {{ stock.recommendation_key }}</div>
                <div class="metric-pill">Earnings: {{ stock.formatted_earnings_date }}</div>
            </div>
        </div>

        <div class="insight-panel">
            <p class="insight-title">Key takeaways</p>
            <div class="insight-list">
                {% for insight in stock.key_insights %}
                <div class="insight-item">
                    <strong>{{ insight.title }}</strong>
                    <p>{{ insight.detail }}</p>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <h2>Daily Price</h2>
                    <span>{{ stock.history_period_label }}</span>
                </div>
                <div class="chart-legend">
                    <span><span class="legend-dot" style="background:#4ad9a1"></span> Close</span>
                </div>
            </div>
            <div class="chart-wrapper">
                <canvas id="priceChart"></canvas>
            </div>
        </div>

        <div class="overview-card">
            <div class="stat">
                <span class="stat__label">Previous close</span>
                <span class="stat__value">{{ stock.formatted_previous_close }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">Today change</span>
                <span class="stat__value">{{ stock.formatted_change_amount }} / {{ stock.formatted_change }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">Open</span>
                <span class="stat__value">{{ stock.formatted_open }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">Day range</span>
                <span class="stat__value">{{ stock.day_range }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">52W range</span>
                <span class="stat__value">{{ stock.fifty_two_week_range }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">Volume</span>
                <span class="stat__value">{{ stock.formatted_volume }}</span>
            </div>
            <div class="stat">
                <span class="stat__label">Avg volume</span>
                <span class="stat__value">{{ stock.formatted_avg_volume }}</span>
            </div>
        </div>

        <details class="details-panel">
            <summary>More data</summary>
            <div class="details-grid">
                <div>
                    <strong>Beta</strong>
                    <div>{{ stock.formatted_beta }}</div>
                </div>
                <div>
                    <strong>Forward P/E</strong>
                    <div>{{ stock.formatted_forward_pe }}</div>
                </div>
                <div>
                    <strong>Profit margin</strong>
                    <div>{{ stock.formatted_profit_margin }}</div>
                </div>
                <div>
                    <strong>Short ratio</strong>
                    <div>{{ stock.formatted_short_ratio }}</div>
                </div>
                <div>
                    <strong>Analyst consensus</strong>
                    <div>{{ stock.formatted_recommendation_mean }}</div>
                </div>
                <div>
                    <strong>Website</strong>
                    <div>{% if stock.website %}<a href="{{ stock.website }}" target="_blank" rel="noreferrer">Visit</a>{% else %}N/A{% endif %}</div>
                </div>
            </div>
        </details>

        <div class="small-row">
            <span>Industry: {{ stock.industry or 'N/A' }}</span>
            <span>Sector: {{ stock.sector or 'N/A' }}</span>
            <span>Exchange: {{ stock.exchange or 'N/A' }}</span>
        </div>

        <div class="summary-card">
            <p class="summary-title">About</p>
            <p class="summary-text">{{ stock.business_summary }}</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script>
        const historyLabels = {{ stock.history_dates | tojson }};
        const historyPrices = {{ stock.history_prices | tojson }};

        const ctx = document.getElementById('priceChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: historyLabels,
                    datasets: [
                        {
                            label: 'Close',
                            data: historyPrices,
                            borderColor: '#4ad9a1',
                            backgroundColor: 'rgba(74, 217, 161, 0.18)',
                            tension: 0.3,
                            pointRadius: 2,
                            borderWidth: 2,
                            fill: true,
                            pointBackgroundColor: '#4ad9a1',
                            pointHoverRadius: 5,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(15, 18, 27, 0.96)',
                            titleColor: '#ffffff',
                            bodyColor: '#cbd0e0',
                            borderColor: 'rgba(255,255,255,0.08)',
                            borderWidth: 1,
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: '#8f95a1' },
                            border: { color: 'rgba(255,255,255,0.08)' }
                        },
                        y: {
                            grid: { color: 'rgba(255,255,255,0.08)' },
                            ticks: { color: '#8f95a1' },
                            border: { color: 'rgba(255,255,255,0.08)' }
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>
"""


def _format_number(value, precision=2):
    if value is None:
        return "N/A"
    try:
        return f"{value:,.{precision}f}"
    except (TypeError, ValueError):
        return str(value)


def _format_currency(value):
    if value is None:
        return "N/A"
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return str(value)


def _format_percent(value):
    if value is None:
        return "N/A"
    try:
        return f"{value:+.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _format_date(value):
    if value is None:
        return "N/A"
    try:
        import datetime
        if isinstance(value, (int, float)):
            return datetime.datetime.fromtimestamp(value).strftime("%b %d, %Y")
        if isinstance(value, str):
            return value
        return str(value)
    except (TypeError, ValueError, OverflowError):
        return str(value)


def _format_large(value):
    if value is None:
        return "N/A"
    try:
        num = float(value)
        for unit in ["", "K", "M", "B", "T"]:
            if abs(num) < 1000.0:
                return f"{num:,.2f}{unit}"
            num /= 1000.0
        return f"{num:.2f}P"
    except (TypeError, ValueError):
        return str(value)


@stock_display_bp.route("/stock/<symbol>")
def stock_detail(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        abort(404)

    ticker = yf.Ticker(symbol)
    info = ticker.info or {}
    if not info:
        abort(404)

    regular_price = info.get("regularMarketPrice") or info.get("previousClose") or 0.0
    prev_close = info.get("regularMarketPreviousClose") or info.get("previousClose") or 0.0
    after_price = info.get("postMarketPrice") or info.get("preMarketPrice")
    after_change = info.get("postMarketChangePercent") or info.get("preMarketChangePercent")
    regular_change = info.get("regularMarketChangePercent")
    session_label = "After Hours" if after_price is not None else "Regular"
    current_price = after_price if after_price is not None else regular_price
    change_percent = after_change if after_price is not None else regular_change

    if change_percent is None and prev_close:
        try:
            change_percent = ((current_price - prev_close) / prev_close) * 100
        except (TypeError, ZeroDivisionError):
            change_percent = 0.0

    recommendation_mean = info.get("recommendationMean")
    if recommendation_mean is None:
        recommendation_mean = info.get("recommendationKey")

    open_price = info.get("open")
    import datetime
    now_ts = datetime.datetime.now().timestamp()
    next_earnings_date = info.get("nextEarningsDate")
    earnings_start = info.get("earningsTimestampStart")
    earnings_end = info.get("earningsTimestampEnd")
    earnings_timestamp = info.get("earningsTimestamp")
    upcoming_earnings = next_earnings_date
    if upcoming_earnings is None:
        future_dates = [d for d in (earnings_start, earnings_end, earnings_timestamp)
                        if isinstance(d, (int, float)) and d > now_ts]
        if future_dates:
            upcoming_earnings = min(future_dates)
        else:
            upcoming_earnings = earnings_start or earnings_end or earnings_timestamp

    history = ticker.history(period="1mo", interval="1d")
    history_dates = []
    history_prices = []
    if not history.empty:
        history_dates = [d.strftime("%b %d") for d in history.index.to_pydatetime()]
        history_prices = [float(v) for v in history["Close"].tolist()]

    def _safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _push_insight(title, detail):
        if detail and len(insight_cards) < 3:
            insight_cards.append({"title": title, "detail": detail})

    insight_cards = []
    short_ratio = _safe_float(info.get("shortRatio"))
    beta_value = _safe_float(info.get("beta"))
    dividend_yield = _safe_float(info.get("dividendYield"))
    profit_margin = _safe_float(info.get("profitMargins"))
    forward_pe = _safe_float(info.get("forwardPE"))
    average_volume = _safe_float(info.get("averageVolume"))
    today_volume = _safe_float(info.get("volume"))
    fifty_two_week_low = _safe_float(info.get("fiftyTwoWeekLow"))
    fifty_two_week_high = _safe_float(info.get("fiftyTwoWeekHigh"))
    volume_ratio = None
    if today_volume and average_volume:
        volume_ratio = today_volume / average_volume

    if change_percent is not None:
        change_percent = _safe_float(change_percent)
        if change_percent is not None:
            abs_change = abs(change_percent)
            if abs_change >= 5:
                direction = "up" if change_percent > 0 else "down"
                _push_insight("Big daily move", f"The stock is {direction} {abs_change:.2f}% today.")
            elif abs_change >= 2:
                _push_insight("Notable intraday move", f"A {abs_change:.2f}% move today indicates stronger market activity.")
            elif abs_change < 0.5:
                _push_insight("Muted session", "Today's trading range is quiet compared with recent volatility.")

    if volume_ratio is not None and len(insight_cards) < 3:
        if volume_ratio >= 1.4:
            _push_insight("Volume is above average", f"Today’s volume is {volume_ratio:.1f}x the average.")
        elif volume_ratio < 0.7:
            _push_insight("Volume is below average", "Trading volume is lighter than usual today.")

    if upcoming_earnings and isinstance(upcoming_earnings, (int, float)) and len(insight_cards) < 3:
        try:
            days_until = int((upcoming_earnings - now_ts) / 86400)
            if 0 <= days_until <= 10:
                _push_insight("Earnings scheduled soon", f"Earnings are due on {_format_date(upcoming_earnings)}.")
        except (TypeError, ValueError):
            pass

    month_change = None
    if not history.empty and len(history) >= 2:
        try:
            start_price = float(history["Close"].iloc[0])
            latest_price = float(history["Close"].iloc[-1])
            if start_price:
                month_change = ((latest_price - start_price) / start_price) * 100
        except (TypeError, ValueError, IndexError):
            month_change = None

    if month_change is not None and len(insight_cards) < 3:
        if month_change >= 10:
            _push_insight("Strong monthly gain", f"The stock has risen {month_change:.2f}% over the past month.")
        elif month_change <= -10:
            _push_insight("Strong monthly decline", f"The stock has fallen {abs(month_change):.2f}% over the past month.")
        elif abs(month_change) < 2:
            _push_insight("Sideways month", "The stock has traded in a narrow range over the last month.")

    if len(insight_cards) < 3 and beta_value is not None:
        if beta_value > 1.4:
            _push_insight("Higher volatility profile", f"Beta is {beta_value:.2f}, which is above market average.")
        elif beta_value < 0.8:
            _push_insight("Lower volatility profile", f"Beta is {beta_value:.2f}, which is below market average.")

    if len(insight_cards) < 3 and forward_pe is not None:
        if forward_pe < 12:
            _push_insight("Low forward P/E", f"Forward P/E is {forward_pe:.2f}.")
        elif forward_pe > 30:
            _push_insight("High forward P/E", f"Forward P/E is {forward_pe:.2f}.")

    if len(insight_cards) < 3 and short_ratio is not None and short_ratio > 2.0:
        _push_insight("High short interest", f"Short ratio is {short_ratio:.2f}.")

    if len(insight_cards) < 3 and dividend_yield is not None and dividend_yield >= 0.03:
        _push_insight("Dividend yield", f"Yield is {dividend_yield:.2%}.")

    if len(insight_cards) < 3 and fifty_two_week_low is not None and fifty_two_week_high is not None and current_price is not None:
        try:
            if current_price <= fifty_two_week_low * 1.05:
                _push_insight("Close to 52-week low", "Price is trading near the 52-week low.")
            elif current_price >= fifty_two_week_high * 0.95:
                _push_insight("Close to 52-week high", "Price is trading near the 52-week high.")
        except (TypeError, ValueError):
            pass

    if not insight_cards:
        _push_insight("No strong signal", "The stock does not show a clear short-term signal right now.")

    history = ticker.history(period="1d", interval="5m", prepost=True)
    history_dates = []
    history_prices = []
    history_period_label = "Today"
    if history.empty:
        history = ticker.history(period="1mo", interval="1d")
        history_period_label = "Past month"

    if not history.empty:
        history_dates = [d.strftime("%H:%M") for d in history.index.to_pydatetime()]
        history_prices = [float(v) for v in history["Close"].tolist()]

    stock_name = info.get("longName") or info.get("shortName") or symbol
    logo_url = info.get("logo_url")
    initials = symbol[:2].upper() if symbol else stock_name[:2].upper()

    stock = {
        "symbol": symbol,
        "name": stock_name,
        "currency": info.get("currency") or "USD",
        "exchange": info.get("exchange") or "",
        "logo_url": logo_url,
        "logo_initials": initials,
        "current_price": current_price,
        "formatted_price": _format_currency(current_price),
        "formatted_change": _format_percent(change_percent),
        "formatted_previous_close": _format_currency(prev_close),
        "formatted_change_amount": _format_currency(current_price - prev_close if current_price is not None and prev_close is not None else None),
        "formatted_open": _format_currency(info.get("open")),
        "day_range": f"{_format_currency(info.get('dayLow'))} – {_format_currency(info.get('dayHigh'))}",
        "fifty_two_week_range": f"{_format_currency(info.get('fiftyTwoWeekLow'))} – {_format_currency(info.get('fiftyTwoWeekHigh'))}",
        "volume": info.get("volume"),
        "formatted_volume": _format_number(info.get("volume"), 0),
        "formatted_avg_volume": _format_number(info.get("averageVolume"), 0),
        "formatted_market_cap": _format_large(info.get("marketCap")),
        "formatted_pe_ratio": _format_number(info.get("trailingPE"), 2),
        "formatted_beta": _format_number(info.get("beta"), 2),
        "formatted_forward_pe": _format_number(info.get("forwardPE"), 2),
        "formatted_profit_margin": _format_percent(info.get("profitMargins") * 100 if info.get("profitMargins") is not None else None),
        "formatted_short_ratio": _format_number(info.get("shortRatio"), 2),
        "formatted_dividend_yield": _format_percent(info.get("dividendYield")),
        "formatted_earnings_date": _format_date(upcoming_earnings),
        "recommendation_key": info.get("recommendationKey") or "N/A",
        "formatted_recommendation_mean": _format_number(recommendation_mean, 2) if isinstance(recommendation_mean, (int, float)) else (recommendation_mean or "N/A"),
        "business_summary": info.get("longBusinessSummary") or "Business summary unavailable.",
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "logo_url": logo_url,
        "logo_initials": initials,
        "session_label": session_label,
        "is_positive": (change_percent or 0.0) >= 0,
        "history_period_label": history_period_label,
        "history_days": len(history_dates),
        "history_dates": history_dates,
        "history_prices": history_prices,
        "key_insights": insight_cards,
    }

    return render_template_string(DETAIL_TEMPLATE, stock=stock)
