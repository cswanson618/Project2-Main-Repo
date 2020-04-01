# Dependencies
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
import pandas as pd
from sqlalchemy import create_engine
import datetime
from .database import connection_string

# Import data into dataframe
df = pd.read_sql(
    "SELECT * FROM plotting",
    con=connection_string, 
    index_col="index"
)

### Bar Graphs ###
max_date = max(df["date"])
max_date_df = df.loc[df["date"] == max_date].copy()

top20_df = max_date_df.sort_values("confirmed", ascending=False)[:20]
confirmed_df = top20_df.sort_values("confirmed", ascending=True)
deaths_df = top20_df.sort_values("deaths", ascending=True)
recovered_df = top20_df.sort_values("recovered", ascending=True)
cf_df = top20_df.sort_values("case_fatality", ascending=True)

# Define Graphic Figures
bar_fig = go.Figure()

trace1 = go.Bar(
    name="Confirmed",
    orientation="h",
    x=list(confirmed_df["confirmed"]),
    y=list(confirmed_df["country_region"]),
    marker={'color': list(confirmed_df["confirmed"]), 'colorscale': 'OrRd'},
    text=list(confirmed_df["confirmed"]),
    texttemplate='%{text: .OF}', 
    hovertemplate='%{y}:%{x: .0F}'
)

trace2 = go.Bar(
    name="Deaths",
    orientation="h",
    x=list(deaths_df["deaths"]),
    y=list(deaths_df["country_region"]),
    marker={'color': list(deaths_df["deaths"]), 'colorscale': 'turbid'},
    text=list(deaths_df["deaths"]),
    texttemplate='%{text: .OF}', 
    hovertemplate = '%{y}:%{x: .0F}',
    visible=False
)

trace3 = go.Bar(
    name="Recovered",
    orientation="h",
    x=list(recovered_df["recovered"]),
    y=list(recovered_df["country_region"]),
    marker={'color': list(recovered_df["recovered"]), 'colorscale': 'Emrld'},
    text=list(recovered_df["recovered"]),
    texttemplate='%{text: .OF}', 
    hovertemplate = '%{y}:%{x: .0F}',
    visible=False
)

trace4 = go.Bar(
    name="Case Fatality",
    orientation="h",
    x=list(cf_df["case_fatality"]),
    y=list(cf_df["country_region"]),
    marker={'color': list(cf_df["case_fatality"]), 'colorscale': 'amp'},
    text=list(cf_df["case_fatality"]),
    texttemplate='%{text: .2F}%', 
    hovertemplate = '%{y}:%{x: .02F}%',
    visible=False
)

# Add Traces
bar_fig.add_trace(trace1)
bar_fig.add_trace(trace2)
bar_fig.add_trace(trace3)
bar_fig.add_trace(trace4)

bar_fig.update_traces(textposition='outside', textfont_size=12)

bar_fig.update_layout(
    title={
        'text': f'Top 20 Countries by COVID-19 Confirmed Cases ({max_date})',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_domain=[0.05, 1.0],
    xaxis= {'showgrid': True},
    font=dict(
        family='-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji',
        size=18,
        color='rgb(119, 88, 2)'),
    showlegend=False,
    height=900,
    paper_bgcolor='rgba(0,0,0,0)'
)

# Add buttons
bar_fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            active=0,
            x=1.15,
            y=0.9,
            buttons=list(
                [
                    dict(
                        label="Confirmed",
                        method="update",
                        args=[
                            {"visible": [True, False, False, False]},
                            {"title": f'Top 20 Countries by COVID-19 Confirmed Cases ({max_date})'},
                        ],
                    ),
                    dict(
                        label="Deaths",
                        method="update",
                        args=[
                            {"visible": [False, True, False, False]},
                            {"title": f'Top 20 Countries by COVID-19 Deaths ({max_date})'},
                        ],
                    ),
                    dict(
                        label="Recovered",
                        method="update",
                        args=[
                            {"visible": [False, False, True, False]},
                            {"title": f'Top 20 Countries by COVID-19 Recovered Cases ({max_date})'},
                        ],
                    ),
                    dict(
                        label="Case Fatality",
                        method="update",
                        args=[
                            {"visible": [False, False, False, True]},
                            {"title": f'Top 20 Countries by COVID-19 Case Fatality Rate ({max_date})'},
                        ],
                    ),
                ]
            ),
        )
    ]
)


### Bubble Chart ###

# Select top 20 countries with the highest number of confirmed cases as of max(date)
top20_countries = list(top20_df["country_region"])
bubble_df = df.loc[df["country_region"].isin(top20_countries)].copy()
bubble_df["older_pop"] = round(bubble_df["older_pop"], 1)
bubble_df["date"] = bubble_df["date"].apply(lambda x: x.strftime('%Y-%m-%d'))
bubble_df = bubble_df.rename(columns = {"country_region":"Country", "date":"Date", "confirmed":"Confirmed", "case_fatality":"Case Fatality", "older_pop":"Older Population"})

# Animated bubble chart
bubble_fig = px.scatter(
    bubble_df, 
    x="Older Population", 
    y="Case Fatality", 
    animation_frame="Date", 
    animation_group="Country",
    size="Confirmed", 
    color="Country",
    size_max=80, 
    range_x=[5,25], 
    range_y=[0,13],
    text="Country",
    
)

bubble_fig.update_traces(
    textposition='top center', 
    textfont={"size":12, "family":"Courier New, monospace"},
)

bubble_fig.update_xaxes(ticksuffix="%")
bubble_fig.update_yaxes(ticksuffix="%")

bubble_fig.update_layout(
    title={
        "text":"<br></br>Do Countries With The Oldest Populatons Have Higher Fatality Rate from COVID-19? <br>",
        'y':1.0,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    margin=dict(t=100),
    font=dict(
        family='-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji',
        size=20,
        color='rgb(119, 88, 2)'),
    xaxis_title="Age 65 and Above (% of Total Population)",
    yaxis_title="Case Fatality Rate (%)",
    showlegend=False,
    height=900,
    paper_bgcolor='rgba(0,0,0,0)',
)

# Save as html
bar_div = plotly.offline.plot(bar_fig, include_plotlyjs=False, output_type='div')
bubble_div = plotly.offline.plot(bubble_fig, include_plotlyjs=False, output_type='div')