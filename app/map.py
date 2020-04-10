#%%
import plotly.graph_objects as go
import plotly.offline
import pandas as pd
from database import connection_string
import datetime as dt
import os

#%%
def load_data():

    df = pd.read_sql("SELECT * FROM plotting", con=connection_string, index_col="index")
    return df


raw_df = load_data()
date_series = raw_df["date"].unique()
max_date = max(date_series)

colorscale_dict = {"confirmed": "Blues", "deaths": "Reds", "recovered": "Greens"}

#%%
confirmed_fig = go.Figure()
# deaths_fig = go.Figure()
# recovered_fig = go.Figure()
#%%
def create_traces(
    fig,
    df,
    confirmed_deaths_recovered,
    date_series=date_series,
    colorscale_dict=colorscale_dict,
):
    for date in date_series:
        trace_df = df[df["date"] == date]
        fig.add_trace(
            dict(
                type="choropleth",
                locations=trace_df["iso3"],
                locationmode="ISO-3",
                z=trace_df[confirmed_deaths_recovered],
                colorscale=colorscale_dict[confirmed_deaths_recovered],
            )
            # go.Choropleth(
            #     locations = trace_df["iso3"],
            #     locationmode = "ISO-3",
            #     z = trace_df[confirmed_deaths_recovered],
            #     text = f"{confirmed_deaths_recovered.title()}",
            #     colorscale = colorscale_dict[confirmed_deaths_recovered],
            # ),
        )

    fig.update_layout(
        title={
            "text": f"COVID-19 {confirmed_deaths_recovered.title()} as of {max(date_series)}",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        autosize=True,
        geo={
            "scope": "world",
            "projection": {"type": "natural earth"},
            "oceancolor": "#3399ff",
            "showcountries": True,
        },
    )


create_traces(confirmed_fig, raw_df, "confirmed")

#%%
def create_slider(fig, confirmed_deaths_recovered, date_series=date_series):
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[
                # make ith trace visible
                {"visible": [date == i for date in range(len(fig.data))]},
            ],
            label=str(date_series[i]),
        )
        steps.append(step)

    sliders = [
        dict(
            active=len(fig.data) - 1,
            currentvalue={"prefix": "Date: "},
            pad={"t": 50},
            steps=steps,
        )
    ]

    fig.update_layout(sliders=sliders)


create_slider(confirmed_fig, "confirmed")
# create_slider(deaths_fig, max_date, "deaths")
# create_slider(recovered_fig, max_date, "recovered")


#%%
confirmed_div = plotly.offline.plot(
    confirmed_fig, include_plotlyjs=False, output_type="div"
)


# %%
with open("file.txt", "w") as write_file:
    write_file.write(confirmed_div)

# %%
