from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
import matplotlib.pyplot as plt
import preprocessor

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['Message Content']:
        words.extend(message.split())

    # Media messages
    num_media_messages = df[df['Message Content'] == '<Media omitted>'].shape[0]

    # Links shared
    links = []
    for message in df['Message Content']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    # Count the number of messages per user
    user_counts = df['User Name'].value_counts().reset_index()
    
    # Rename columns: 'index' -> 'User Name', 'User Name' -> 'Message Count'
    user_counts.columns = ['User Name', 'Message Count']
    
    # Calculate the percentage of total messages for each user
    user_counts['Percentage'] = round((user_counts['Message Count'] / df.shape[0]) * 100, 2)
    
    # Only return the 'User Name' and 'Percentage' columns
    return user_counts[['User Name', 'Percentage']]


def create_wordcloud(selected_user, df):
    def remove_stop_words(text):
        f = open('stop_hinglish.txt', 'r')
        stop_words = set(f.read().split())
        f.close()

        filtered_words = [word for word in text.split() if word.lower() not in stop_words]
        return ' '.join(filtered_words)

    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]

    # Combine all messages into a single text
    combined_text = df['Message Content'].str.cat(sep=" ")
    
    # Remove stop words
    filtered_text = remove_stop_words(combined_text)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(filtered_text)
    return df_wc


def most_common_words(selected_user, df):
    def remove_stop_words(text):
        f = open('stop_hinglish.txt', 'r')
        stop_words = set(f.read().split())
        f.close()

        filtered_words = [word for word in text.split() if word.lower() not in stop_words]
        return filtered_words

    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]

    temp = df[df['Message Content'] != '<Media omitted>\n']

    words = []

    for message in temp['Message Content']:
        words.extend(remove_stop_words(message))

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return most_common_df


def analyze_emojis(selected_user, df):
    def extract_emojis(text):
        return ''.join(c for c in text if c in emoji.EMOJI_DATA)

    if selected_user != 'Overall':
        df = df[df['User Name'] == selected_user]

    # Extract emojis from all messages
    emojis = []
    for message in df['Message Content']:
        emojis.extend(extract_emojis(message))

    # Count emoji frequencies
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count']).sort_values(by='Count', ascending=False)

    return emoji_df


def plot_monthly_timeline(df):
    monthly_data = preprocessor.monthly_timeline(df)
    
    fig, ax = plt.subplots()
    ax.plot(monthly_data['Date'], monthly_data['Message Count'], marker='o', linestyle='-', color='b')
    ax.set_title('Monthly Timeline of Messages')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Messages')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    return fig


# helper.py

import matplotlib.pyplot as plt
import preprocessor

def plot_daily_timeline(df):
    daily_data = preprocessor.daily_timeline(df)
    
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the size as needed
    ax.plot(daily_data['Date'], daily_data['Message Count'], marker='o', linestyle='-', color='r')
    ax.set_title('Daily Timeline of Messages')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Messages')
    plt.xticks(rotation=45)
    
    return fig
