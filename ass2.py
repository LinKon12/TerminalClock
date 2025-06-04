import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017/")
db = client["air_quality_db"]
collection = db["air_quality_timeseries"]
weekly_collection = db["weekly_avg_values"]

collection.drop()
weekly_collection.drop()

df = pd.read_csv("AirQualityUCI.csv", sep=';', decimal=',')

df = df.drop(columns=['Unnamed: 15', 'Unnamed: 16'], errors='ignore')

df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')

df = df.dropna(subset=['datetime'])

df = df.rename(columns={"CO(GT)": "CO_GT"})

df = df[['datetime', 'CO_GT']]

df = df[df["CO_GT"] != -200]

df = df.sort_values(by='datetime')

db.create_collection("air_quality_timeseries", timeseries={"timeField": "datetime", "metaField": None})

collection.insert_many(df.to_dict("records"))

data = list(collection.find({}))
df_mongo = pd.DataFrame(data)
df_mongo.set_index("datetime", inplace=True)

df_numeric = df_mongo.select_dtypes(include=['number'])

plt.figure(figsize=(12, 4))
plt.plot(df_mongo.index, df_mongo["CO_GT"], label="CO(GT)")
plt.title("CO(GT) Over Time")
plt.xlabel("Time")
plt.ylabel("CO concentration")
plt.legend()
plt.tight_layout()
plt.show()

print("Mean:", df_numeric["CO_GT"].mean())
print("Median:", df_numeric["CO_GT"].median())
print("Standard Deviation:", df_numeric["CO_GT"].std())

weekly_df = df_numeric.resample("W").mean()

weekly_data = weekly_df.reset_index().to_dict("records")
weekly_collection.insert_many(weekly_data)

plt.figure(figsize=(12, 4))
plt.plot(df_mongo.index, df_mongo["CO_GT"], alpha=0.4, label="Raw CO(GT)")
plt.plot(weekly_df.index, weekly_df["CO_GT"], color='red', label="Weekly Avg")
plt.title("Weekly Average CO(GT) Over Time")
plt.xlabel("Time")
plt.ylabel("CO concentration")
plt.legend()
plt.tight_layout()
plt.show()

'''
Trend identification:
I have plotted CO ( Carbon Monooxide )levels against time using UCI Air Quality dataset
There is increased CO levels in colder months and slightly less in hotter months of the year
The sudden spike to 0 indicates missing data

'''