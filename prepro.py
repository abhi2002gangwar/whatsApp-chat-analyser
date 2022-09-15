import re
import pandas as pd

def preprocess(data):
    pattern = '(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s?[AP][M])\s-\s'

    messages = re.split(pattern, data)[::2]
    messages = messages[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'usr_msg': messages, 'msg_dts': dates})

    df['msg_dts'] = pd.to_datetime(df['msg_dts'], format='%m/%d/%y, %H:%M %p')

    df.rename(columns={'msg_dts': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['usr_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('grp_notification')
            messages.append(entry[0])
            
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['usr_msg'], inplace=True)

    df['_date_'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['monthnum'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name().str.slice(stop=3)
    df['daynum'] = df['date'].dt.day
    df['day'] = df['date'].dt.day_name().str.slice(stop=3)
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + '-' + str('1'))
        elif hour == 0:
            period.append(str('1') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df