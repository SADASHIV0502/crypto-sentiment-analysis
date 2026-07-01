import os
import matplotlib.pyplot as plt
import seaborn as sns


from src.loader import load_sentiment_data, load_trading_data, merge_datasets
from src.analytics import calculate_sentiment_performance, analyze_directional_bias

def main():
    print("--- Starting Analytics Engine ---")
    
    
    sentiment_path = os.path.join('data', 'fear_greed_index.csv')
    trading_path = os.path.join('data', 'historical_data.csv')
    

    print("Loading and normalizing datasets...")
    try:
        sentiment_df = load_sentiment_data(sentiment_path)
        trading_df = load_trading_data(trading_path)
        merged_df = merge_datasets(trading_df, sentiment_df)
        print(f"Success: Matched {len(merged_df)} trading records with market sentiment.\n")
    except FileNotFoundError as e:
        print(f"Error: Could not find data files. Make sure they are in the 'data' folder. Details: {e}")
        return

    # Run Analytics
    print("--- Performance Breakdowns by Market Sentiment ---")
    perf_metrics = calculate_sentiment_performance(merged_df)
    print(perf_metrics.to_string(index=False))
    print("\n")
    
    print("--- Trade Direction Bias (%) ---")
    bias_metrics = analyze_directional_bias(merged_df)
    print(bias_metrics.round(2))
    print("\n")
    
    # Generate Visualizations (Two Main Graphs)
    print("Generating visual charts...")
    sns.set_theme(style="whitegrid")
    
   
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=perf_metrics, 
        x='Sentiment', 
        y='Total PnL', 
        hue='Sentiment',
        palette='RdYlGn', 
        legend=False
    )
    plt.title('Graph 1: Net Profitability (PnL) by Market Sentiment', fontsize=14, pad=15)
    plt.xlabel('Market Sentiment Phase', fontsize=12)
    plt.ylabel('Cumulative Closed PnL (USD)', fontsize=12)
    plt.tight_layout()
    plt.savefig('Graph1_Performance_vs_Sentiment.png', dpi=300)
    plt.show()
    
    # "Hidden Pattern" (Risk & Position Sizing)
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=perf_metrics, 
        x='Sentiment', 
        y='Avg Trade Size (USD)', 
        marker='o',
        color='purple',
        linewidth=2.5,
        markersize=10
    )
    plt.title('Graph 2: Hidden Pattern - Average Trade Size (Risk) per Phase', fontsize=14, pad=15)
    plt.xlabel('Market Sentiment Phase', fontsize=12)
    plt.ylabel('Average Capital Risked per Trade (USD)', fontsize=12)
    
    
    plt.fill_between(perf_metrics['Sentiment'], perf_metrics['Avg Trade Size (USD)'], alpha=0.2, color='purple')
    plt.tight_layout()
    plt.savefig('Graph2_Hidden_Risk_Pattern.png', dpi=300)
    plt.show()

    print("Generating Graph 3...")
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=perf_metrics, 
        x='Sentiment', 
        y='Win Rate (%)', 
        palette='Blues',
        hue='Sentiment',
        legend=False
    )
    
    plt.axhline(y=50, color='red', linestyle='--', alpha=0.7)
    
    plt.title('Graph 3: Trader Accuracy (Win Rate) per Sentiment Phase', fontsize=14, pad=15)
    plt.xlabel('Market Sentiment Phase', fontsize=12)
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.tight_layout()
    plt.savefig('Graph3_Win_Rate_Precision.png', dpi=300)
    plt.show()

    #Directional Bias (Herd Mentality)
    print("Generating Graph 4...")
    
    bias_metrics.plot(
        kind='bar', 
        stacked=True, 
        figsize=(10, 6), 
        colormap='coolwarm',
        edgecolor='black'
    )
    plt.title('Graph 4: Directional Bias (Long vs. Short) by Sentiment', fontsize=14, pad=15)
    plt.xlabel('Market Sentiment Phase', fontsize=12)
    plt.ylabel('Percentage of Total Trades (%)', fontsize=12)
    
    
    plt.legend(title='Trade Direction', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('Graph4_Directional_Bias.png', dpi=300)
    plt.show()

    print("Analysis complete! Two graphs saved locally.")

if __name__ == '__main__':
    main()