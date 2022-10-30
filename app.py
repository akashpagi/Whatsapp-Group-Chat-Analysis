import streamlit as st # pip install streamlit
import preprocessor , helper # pip install preprocessor
import matplotlib.pyplot as plt

# for running the streamlit app use this command "streamlit run app.py"
st.sidebar.title('Whats App Chat Analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    
    #converting file data into string format
    data = bytes_data.decode('utf-8')

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch group users unique values and show them on sidebar 

    # taking user column unique value and convertrd into list 
    user_list = df['user'].unique().tolist()

    # removing group notification
    user_list.remove('group_notification')

    # sort the number and alphabets
    user_list.sort()

    # insert in user list at 0 position name as overall
    user_list.insert(0,'Overall')

    # added into side bar 
    selected_user = st.sidebar.selectbox('Show Users From Group : ',user_list)

    if st.sidebar.button('Show Analysis'):
        # analysis part
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
   
        #1 create beta 4 colunms
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:             
            st.subheader('Total Messages')         
            st.subheader(num_messages)

        with col2:
            st.subheader('Total Words')         
            st.subheader(words)  

        with col3:  
            st.subheader('Shared Media')        
            st.subheader(num_media_messages)

        with col4:
            st.subheader('Shared Links')         
            st.subheader(num_links)


        # Finding the top 5 most active user and Show their percentages of activity in group
        if selected_user == 'Overall':
            st.header('# Most Active Users ')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()           
            col1, col2 = st.columns(2) 

            with col1: 
                st.text('Top 5 most active users in group')              
                ax.bar(x.index, x.values, width=0.6)
                plt.xlabel("Users")
                plt.ylabel("Message Counts")
                plt.xticks(rotation='vertical')
                plt.title("Top 5 Active Users") #<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True
                st.pyplot(fig)
           
            with col2:
                st.text('User messages in percentage')
                st.dataframe(new_df)
        
        
        # WordCloud 
        st.header('# WordCloud')      
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()         
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # most common words
        st.header('# Most Common Words')   
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots() 
                
        ax.barh(most_common_df[0],most_common_df[1]) # .barh means horizontal bar 
        ax.grid(b = True, color ='green',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        # Emojis Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)
        
        