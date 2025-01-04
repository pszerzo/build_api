from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("data_small/stations.txt", skiprows=17)
df = df[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", data=df.to_html())


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["   TG"] = df["   TG"] / 10
    df = df[["STAID", "    DATE", "   TG"]]
    return render_template("station.html", data=df.to_html())


@app.route("/api/v1/yearly/<station>/<year>")
def flex_date(station, year):
    filename = "data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    df['   TG'] = df['   TG'] / 10
    df = df.loc[df['    DATE'].str.startswith(year)][['STAID', '    DATE', '   TG']]
    return render_template("station.html", data=df.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return{"station": station,
           "date": date,
           "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True, port=5000) # default: port=5000, if you want to run multiple you need to change
