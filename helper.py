import nltk
import pandas as pd

from collections import Counter
def fetch_total_messages(selected_user,df):
    nltk.download('punkt')
    if selected_user=="Overall":
        return df.shape[0]
    else:
        return  df[df["users"]==selected_user].shape[0]

def fetch_total_words(selected_user,df):
    import nltk
    if selected_user=="Overall":
        mes=len(nltk.word_tokenize(df["message"].to_string()))
        return mes
    else:
        mes=df[df["users"]==selected_user]["message"].to_string()
        length_words=len( nltk.word_tokenize(mes))
        return  length_words

def fetch_total_emoji(selected_user,df):
    import re

    # Define a regular expression pattern to match a broader range of emojis
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF\U0001F600-\U0001F64F\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF]+')


    if selected_user=="Overall":
        emo=re.findall(emoji_pattern,df["message"].to_string())
        return len(emo)
    else:
        emojis = re.findall(emoji_pattern,df[df["users"]==selected_user]["message"].to_string())
        return len(emojis)

def media(selected_user,df):

        if selected_user=="Overall":

            num=df[df["message"]=="<Media omitted>\n"].shape[0]
            return num

        else:
            df=df[df["users"]==selected_user]
            num1=df[df["message"]=="<Media omitted>\n"].shape[0]
            return num1

def links(selected_user,df):
    from urlextract import URLExtract
    extract=URLExtract()
    if selected_user == "Overall":
        link=[]
        for message in df["message"]:
            link.extend(extract.find_urls(message))
        return len(link)


    else:
        df = df[df["users"] == selected_user]
        link1 = []
        for message in df["message"]:
            link1.extend(extract.find_urls(message))
        return len(link1)



def acitivty(df):
    import matplotlib.pyplot as plt
    x=df["users"].value_counts().head()
    df=round((df["users"].value_counts() / len(df)) * 100, 2).reset_index().rename(columns={"index": "name", "users": "percentage"})

    return x,df

def wordcloud(selected_user,df):
    from nltk.corpus import stopwords
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    stop = set(stopwords.words('english'))
    stop.update(
        ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '@', '#', 'rt', 'amp', 'realdonaldtrump',
         'http', 'https', '/', '://', '_', 'co', 'trump', 'donald', 'ho','ko','jo','omitted','-','<','>','*','h','bhi','hai','?'])

    if selected_user!="Overall":
        df=df[df["users"]==selected_user]

    messages=df["message"].str.cat(sep=" ")

    list_of_words=[i.lower() for i in nltk.wordpunct_tokenize(messages) if i not in stop and i not in stop_words]
    wordfreq=nltk.FreqDist(list_of_words)
    most_common=wordfreq.most_common(30)
    return most_common

def emoji_data(selected_user,df):
    import emoji


    if selected_user!="Overall":
        df=df[df["users"]==selected_user]

    emojis=[]
    for message in df["message"]:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    timeline = df.groupby(["year", "month_name", "month"]).count()["message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month_name"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    df["only_date"]=df["date"].dt.date
    timeline_Daily=df.groupby("only_date").count()["message"].reset_index()
    return  timeline_Daily

def week_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    return  df["day_name"].value_counts()

def month_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    return df["month_name"].value_counts()

def acitivity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    user_heatmap=df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)
    return user_heatmap
