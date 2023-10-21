import streamlit as st
import nltk
nltk.download('punkt')
import preprocessing,helper
import matplotlib.pyplot as plt
import  seaborn as sns
from wordcloud import  WordCloud
st.sidebar.header("Whatsapp chat analysis")

upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessing.preprossing(data)



    user_list=df["users"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("show analysis of",user_list)
    if st.sidebar.button("show analysis"):
        st.title("Top Statistics")
        col1,col2,col3,col4,col5=st.columns(5)

        with col1:

            st.header("Total messages ")
            num_messages = helper.fetch_total_messages(selected_user, df)

            st.title(num_messages)

        with col2:
            st.header("total words")
            num_words=helper.fetch_total_words(selected_user,df)
            st.title(num_words)

        with col3:
            st.header("emojis")
            num_emoji=helper.fetch_total_emoji(selected_user,df)
            st.title(num_emoji)

        with col4:
            st.header("media")
            media1=helper.media(selected_user,df)
            st.title(media1)

        with col5:
            st.title("links")
            l1=helper.links(selected_user,df)
            st.title(l1)

        col1,col2=st.columns(2)
        with col1:
            st.title("montly anlysis")
            timeline=helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline["time"], timeline["message"],color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.title("daily anlysis")
            timeline_daily=helper.daily_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline_daily["only_date"],timeline_daily["message"])
            st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most Busy Users")
            col1,col2=st.columns(2)
            x,new_df=helper.acitivty(df)
            fig,ax=plt.subplots()

            with col1:
                plt.bar(x.index,x.values,color="red")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


    wc= helper.wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    plt.barh(range(len(wc)),[var[1]for var in wc])
    plt.yticks((range(len(wc))),[var[0] for var in wc])

    st.pyplot(fig)

    col1,col2=st.columns(2)
    with col1:
        st.title("emojis")
        emoji_df=helper.emoji_data(selected_user,df)
        st.dataframe(emoji_df)

    with col2:
        st.title("pie chat")
        fig,ax=plt.subplots()

        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)


    st.title("Activity Map")
    col1,col2=st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day=helper.week_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month=helper.month_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

    st.header("Weekly activity map")
    activity_heatmap = helper.acitivity_heatmap(selected_user, df)
    fig,ax = plt.subplots()
    ax=sns.heatmap(activity_heatmap)
    st.pyplot(fig)










