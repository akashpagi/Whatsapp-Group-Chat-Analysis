import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Group Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis With respect to",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.title(num_links)
        
        st.markdown("""---""")

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='lightgreen')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map (Heatmap)")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, linewidth=1, linecolor='black', square=True, cmap='Blues', cbar_kws={'label': 'Colorbar for Heatmap', 'orientation': 'horizontal'}) #annot=True
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            plt.xlabel("Group users")
            plt.ylabel("Messages")
            
            #col1, col2 = st.columns(2)
            col1,col2 = st.columns([2,3])
            with col1:
                st.title('Most Busy Users')
                ax.bar(x.index, x.values,color='skyblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.title('Messages Contribution') 
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        plt.xlabel("Meassages (words) count")
        plt.ylabel("Common words in chat")
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)









