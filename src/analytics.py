import pandas as pd

def calculate_sentiment_performance(merged_df):
   
    summary = []
    
    # Group the historical trades by the daily market sentiment classification
    grouped = merged_df.groupby('classification')
    
    for sentiment, group in grouped:
        total_trades = len(group)
        if total_trades == 0:
            continue
            
        # A trade is considered a win if the Closed PnL is positive
        winning_trades = group[group['Closed PnL'] > 0]
        win_rate = len(winning_trades) / total_trades
        
        total_pnl = group['Closed PnL'].sum()
        avg_trade_size = group['Size USD'].mean()
        
        summary.append({
            'Sentiment': sentiment,
            'Total Trades': total_trades,
            'Win Rate (%)': round(win_rate * 100, 2),
            'Total PnL': round(total_pnl, 2),
            'Avg Trade Size (USD)': round(avg_trade_size, 2)
        })
        
    return pd.DataFrame(summary)

def analyze_directional_bias(merged_df):
    
    bias_table = pd.crosstab(merged_df['classification'], merged_df['Side'], normalize='index') * 100
    
    return bias_table