def fetch_news(api_endpoint, keywords, interval):
    news_articles = []

    while True:
        try:
            response = request.get(api_endpoint, params={'q': keywords, 'interval': interval})
            if response.status_code == 200:
                data = response.json()
                articles = response.json().get('articles', [])
                for article in articles:
                    news_article = {
                        "title": article["title"],
                        "content": article["content"],
                        "timestamp": article["publishedAt"]}
                    news_articles.append(news_article)
            else:
                print("Failed to fetch news data, status: ", response.status_code)
        except request.exceptions.RequestException as e:
            print("Network error: ", e)
            time.sleep(interval)

            continue
        
        time.sleep(interval)
        
        return news_articles
    




def analyze_sentiment(news_article):
    try:
        content = preprocess_content(news_article["content"])
        sentiment_model = load_sentiment_model()
        sentiment_score = sentiment_model.analyze(content)

        if sentiment_score < 0:
            label = "Negative"
        elif sentiment_score == 0:
            label = "Neutral"
        else:
            label = "Positive"
    except ModelError as e:
        print("Sentiment analysis failed:", e)
        sentiment_score = 0  # Default to neutral if analysis fails
        label = "Neutral"

    return sentiment_score, label




def generate_signal(sentiment_score, market_data, buy_threshold, sell_threshold):
    if sentiment_score >= buy_threshold and market_data["trend"] == "up":
        trade_signal = "Buy"
    elif sentiment_score <= sell_threshold and market_data["trend"] == "down":
        trade_signal = "Sell"
    else:
        trade_signal = "Hold"

    return trade_signal





def execute_trade(trade_signal, account_data, position_size, tp, sl):
    if trade_signal not in ["Buy", "Sell"]:
        print("No trade signal.")
        return "No Action"

    try:
        broker_api = connect_to_broker_api()
        order_type = "Market"
        order_size = calculate_position_size(account_data, position_size)

        trade_order = broker_api.place_order(
            action=trade_signal,
            order_type=order_type,
            size=order_size,
            take_profit=tp,
            stop_loss=sl
        )

        if trade_order.success:
            log_trade(trade_order)
            return "Trade Executed"
        else:
            print("Trade execution failed:", trade_order.error_message)
            return "Execution Failed"
    except APIConnectionError as e:
        print("Broker API connection error:", e)
        return "Execution Failed"




def calculate_position_size(account_balance, risk_per_trade, asset_price):
    try:
        position_size = (account_balance * risk_per_trade) / (asset_price * RISK_FACTOR)
        if position_size > MAX_ALLOWED_POSITION:
            position_size = MAX_ALLOWED_POSITION
        elif position_size < MIN_ALLOWED_POSITION:
            print("Position size too small")
            position_size = 0  # Skip trade due to low balance
    except ZeroDivisionError:
        print("Error in position size calculation")
        position_size = 0

    return position_size

def enforce_risk_management(trade_order, current_market_price, sl, tp):
    if current_market_price <= sl:
        close_position(trade_order)
        print("Stop-loss triggered")
    elif current_market_price >= tp:
        close_position(trade_order)
        print("Take-profit triggered")

    return trade_order





def log_trade(trade_order):
    try:
        with open("trade_log.txt", "a") as log_file:
            log_file.write(f"{trade_order['timestamp']}, {trade_order['action']}, {trade_order['entry_price']}, {trade_order['exit_price']}, {trade_order['pnl']}\\n")
        return "Trade logged successfully"
    except IOError as e:
        print("Trade logging failed:", e)
        return "Log Failure"

def calculate_performance_metrics(trade_log):
    total_profit = 0
    total_wins = 0
    total_trades = len(trade_log)

    for trade in trade_log:
        if trade["pnl"] > 0:
            total_wins += 1
        total_profit += trade["pnl"]

    win_rate = total_wins / total_trades if total_trades > 0 else 0
    average_profit = total_profit / total_trades if total_trades > 0 else 0

    return {"Total Profit": total_profit, "Win Rate": win_rate, "Average Profit": average_profit}
