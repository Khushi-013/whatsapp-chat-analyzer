import pandas as pd
import re

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\u202F[APMapm]{2}) - (.*?): (.*)'
    messages = re.findall(pattern, data)
    df = pd.DataFrame(messages, columns=['Date', 'Time', 'User', 'Message'])
    
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
    
    # Check if 'Date' column conversion was successful
    if df['Date'].isnull().all():
        raise ValueError("Date conversion failed. Please check the date format in your data.")
    
    # Additional columns
    df['Date_Time'] = df['Date'].dt.strftime('%m/%d/%y') + ', ' + df['Time']
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = pd.to_datetime(df['Time'], format='%I:%M %p').dt.hour
    df['Minute'] = pd.to_datetime(df['Time'], format='%I:%M %p').dt.minute
    df = df[['Date_Time', 'User', 'Message', 'Year', 'Month', 'Day', 'Hour', 'Minute']]
    df.columns = ['Date and Time', 'User Name', 'Message Content', 'Year', 'Month', 'Day', 'Hour', 'Minute']
    
    return df


import pandas as pd

def monthly_timeline(df):
    # Ensure the 'Date' column is correctly named
    if 'Date and Time' not in df.columns:
        raise KeyError("The DataFrame does not contain a 'Date and Time' column.")
    
    # Convert 'Date and Time' to datetime format
    df['Date'] = pd.to_datetime(df['Date and Time'], format='%m/%d/%y, %I:%M %p', errors='coerce')
    
    if df['Date'].isnull().all():
        raise ValueError("Date conversion failed. Please check the date format in your data.")
    
    # Group by month and year, and count the number of messages
    monthly_data = df.groupby(df['Date'].dt.to_period('M')).size().reset_index(name='Message Count')
    monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()  # Convert period to timestamp

    return monthly_data


# preprocessor.py

import pandas as pd

def daily_timeline(df):
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Group by date and count messages
    daily_data = df.groupby(df['Date'].dt.date).size().reset_index(name='Message Count')
    daily_data['Date'] = pd.to_datetime(daily_data['Date'])
    
    return daily_data
