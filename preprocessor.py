import re
import pandas as pd

def preprocess(data):
    # for checking of regular expression visit this site > https://regex101.com/
    pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s' # 12Hours pattern s means space
    #pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s' #for 24hrs format chat file
    #pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'

    messages = re.split(pattern, data)[1:] # for slicing we use [1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    #converting messages_date type in date format
    #https://dataindependent.com/pandas/pandas-to-datetime-string-to-date-pd-to_datetime/
    df['message_date'] = pd.to_datetime(df['message_date'], format ='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'}, inplace=True) # rename the dates name as 'date'

    #seprate users and messages from user_messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
