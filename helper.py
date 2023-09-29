from urlextract import URLExtract
extract = URLExtract
from wordcloud import WordCloud

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    num_messages = df.shape[0]
    positive_message = df["positive"].sum()
    negative_message = df["negative"].sum()
    neutral_message = df["neutral"].sum() - num_media_messages

    r_positive = round(positive_message, 3)
    r_negative = round(negative_message, 3)
    r_neutral = round(neutral_message, 3)

    return num_messages,r_positive,r_negative,r_neutral

def media(df):
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_media_messages


def create_wordcloud(selected_user, df):
    if selected_user == "Overall":
        filtered_df = df
    else:
        filtered_df = df[df['user'] == selected_user]

    # Convert non-string messages to string
    filtered_df['message'] = filtered_df['message'].astype(str)

    # Generate word cloud
    messages = filtered_df['message'].str.cat(sep=" ")

    if messages.strip():  # Check if there are messages to generate a word cloud
        wc = WordCloud(width=800, height=400, background_color='white').generate(messages)
        return wc
    else:
        return None
