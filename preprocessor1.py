import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ', errors='raise')
    except ValueError as e:
        print(f"Error: {e}")
        df['message_date'] = pd.to_datetime(df['message_date'].str.replace(', ', ''), format='%m/%d/%y, %H:%M - ',
                                            errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    df["positive"] = [sid.polarity_scores(i)["pos"] for i in df["message"]]
    df["negative"] = [sid.polarity_scores(i)["neg"] for i in df["message"]]
    df["neutral"] = [sid.polarity_scores(i)["neu"] for i in df["message"]]

    return df
