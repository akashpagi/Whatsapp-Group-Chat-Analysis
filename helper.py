from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

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
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name' , 'user':'percentage (%)'})
    return x,df

def create_wordcloud(selected_user, df):  
        
    # remove stop words
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # remove group notification
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    # creating nested function
    #removing Hinglish stop words
    def remove_stop_stops(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
        
    # creating object of wordcloud class
    wc = WordCloud(width=280, height=280, min_font_size=5, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_stops)
    #wc.generate a image of wordcloud
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    # remove stop words
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall': 
        df = df[df['user'] == selected_user]
    
    # remove group notification
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []
    for message in temp['message']:
    #visit every msg then converting the msg into lower case fetch the words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    #we have to import Counter form collections and with the help of counter findout the frequency of words
    most_common_df = pd.DataFrame(Counter(words).most_common(20)) 
    return most_common_df 











