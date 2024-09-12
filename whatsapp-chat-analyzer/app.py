import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar Title
st.sidebar.title("WhatsApp Chat Analysis")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload a file")

# Check if a file is uploaded
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    # Preprocess the data
    df = preprocessor.preprocess(data)
    
    # Display the processed DataFrame in Streamlit
    st.dataframe(df)  # This will display the DataFrame in a tabular format

    user_list = df['User Name'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetch statistics for selected user or overall
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        
        st.title('Top Statistics')
        # Display the statistics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Show most busy users if 'Overall' is selected
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            new_df = helper.most_busy_users(df)
            
            # Plot bar chart of most busy users
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                # Use 'User Name' and 'Percentage' columns for plotting
                ax.bar(new_df['User Name'], new_df['Percentage'], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)  # Display DataFrame with user names and percentage

        # Show word cloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Plot the most common words using column names, not indices
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        
        # Use column names: 'Word' and 'Frequency'
        ax.barh(most_common_df['Word'], most_common_df['Frequency'], color='yellow')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Show emoji analysis
        emoji_df = helper.analyze_emojis(selected_user, df)
        
        # Create columns for pie chart and table
        col1, col2 = st.columns(2)

        with col1:
            st.title("Emoji Analysis")
            # Plot emoji percentages as a pie chart
            fig, ax = plt.subplots()
            emojis = emoji_df['Emoji']
            counts = emoji_df['Count']
            total = sum(counts)
            percentages = [(count / total) * 100 for count in counts]
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                percentages, 
                labels=[f'{e} {p:.1f}%' for e, p in zip(emojis, percentages)],
                autopct='%1.1f%%',
                colors=plt.get_cmap('tab20').colors,
                startangle=140
            )
            
            # Set font size for labels and percentages
            for text in texts:
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_fontsize(10)
            
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            
            st.pyplot(fig)

        with col2:
            st.title('Emoji Usage')
            st.dataframe(emoji_df)

        # Plot monthly and daily timelines
        st.title('Monthly and Daily Timelines')

        # Monthly Timeline
        fig = helper.plot_monthly_timeline(df)
        st.subheader('Monthly Timeline of Messages')
        st.pyplot(fig)

        # Daily Timeline
        fig = helper.plot_daily_timeline(df)
        st.subheader('Daily Timeline of Messages')
        st.pyplot(fig)

        # Activity Map: Most Busy Month and Most Busy Day
        st.title('Activity Map: Most Busy Month and Day')

        # Plot most busy month
        monthly_data = preprocessor.monthly_timeline(df)
        most_busy_month = monthly_data.loc[monthly_data['Message Count'].idxmax()]
        
        fig, ax = plt.subplots()
        ax.bar(most_busy_month['Date'].strftime('%Y-%m'), most_busy_month['Message Count'], color='blue')
        ax.set_title('Most Busy Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Messages')
        st.pyplot(fig)

        # Plot most busy day
        daily_data = preprocessor.daily_timeline(df)
        most_busy_day = daily_data.loc[daily_data['Message Count'].idxmax()]
        
        fig, ax = plt.subplots()
        ax.bar(most_busy_day['Date'].strftime('%Y-%m-%d'), most_busy_day['Message Count'], color='green')
        ax.set_title('Most Busy Day')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Messages')
        st.pyplot(fig)

        # Activity Heat Map
        st.title('Activity Heat Map')

        # Generate heat map data
        df['Hour'] = df['Date'].dt.hour
        df['Day of Week'] = df['Date'].dt.day_name()
        
        # Pivot table for heat map
        heatmap_data = df.pivot_table(index='Day of Week', columns='Hour', aggfunc='size', fill_value=0)
        
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5, ax=ax)
        ax.set_title('Activity Heat Map')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Day of Week')
        st.pyplot(fig)
