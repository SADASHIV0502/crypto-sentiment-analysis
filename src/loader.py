import pandas as pd

def load_sentiment_data(filepath):

    df = pd.read_csv(filepath)
    
   
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    
    return df[['date', 'value', 'classification']]

def load_trading_data(filepath):
    
    df = pd.read_csv(filepath)
    
    # The timestamps are in local IST format (DD-MM-YYYY HH:MM)
    
    df['parsed_time'] = pd.to_datetime(df['Timestamp IST'], format='%d-%m-%Y %H:%M')
    df['date'] = df['parsed_time'].dt.date
    
    # Clean up financial columns: force them into numbers and fill blanks with 0 to prevent math errors
    df['Closed PnL'] = pd.to_numeric(df['Closed PnL'], errors='coerce').fillna(0)
    df['Size USD'] = pd.to_numeric(df['Size USD'], errors='coerce').fillna(0)
    
    return df

def merge_datasets(trading_df, sentiment_df):
    
    # An 'inner' merge ensures we only keep trades that have matching sentiment data for that day
    merged_df = pd.merge(trading_df, sentiment_df, on='date', how='inner')
    
    return merged_df