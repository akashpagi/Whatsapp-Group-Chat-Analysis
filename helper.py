from urlextract import URLExtract

# creating object for extract 
extract = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1.fetch number of messages
    num_messages = df.shape[0]-1
    # 2.number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch number of links shared
    # install urlextract : pip install urlextract 
    # it will helps us to find the links in particular columns
    links = [] # list
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return num_messages, len(words), num_media_messages, len(links)

# Finding the top 5 most active user & plot bar and Show their percentages of activity in group 
def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name' , 'user':'percent'})
    return x,df




















'''
        # 1.fetch number of messages
        num_messages = df.shape[0]

        # 2.number of words
        words = []
        for message in df['message']:
            words.extend(message.split())
        return num_messages, len(words) 
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        return num_messages, len(words)


 


        df = [df['user'] == selected_user]

    num_messages = df.shape[0]    
    words = []
    for message in df['message']:
        words.extend(message.split())

    return num_messages,len(words)
 
   '''      