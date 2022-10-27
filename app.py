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

        with col3:
            st.subheader('Shared Links')         
            st.subheader(num_links)


        # Finding the top 5 most active user and Show their percentages of activity in group
        if selected_user == 'Overall':
            st.title('Most Active Users ')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()           
            col1, col2 = st.columns(2) 

            with col1:               
                ax.bar(x.index, x.values, width=0.6)
                plt.xlabel("Users")
                plt.ylabel("Messages Counts")
                plt.xticks(rotation='vertical')
                plt.title("Top 5 Active Users")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
