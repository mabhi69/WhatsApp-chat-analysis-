import re
import pandas as pd
def preprossing(data):

    pattern = "\d{1,2}/\d{1,2}/\d{0,2},\s\d{1,2}:\d{2}\s-\s"
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_message": message, "message_date": dates})

    # Parse the date and time with the century included
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %H:%M - ")

    # Rename the column if needed
    df.rename(columns={"message_date": "date"}, inplace=True)

    users = []
    messagex = []
    for message in df["user_message"]:
        entry = re.split("^([^:]+):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messagex.append(entry[2])
        else:
            users.append("group_notification")
            messagex.append(entry[0])

    df["users"] = users
    df["message"] = messagex
    df.drop(columns=["user_message"], inplace=True)
    df["month_name"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_name"] = df["date"].dt.day_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"]=period
    return df


    
