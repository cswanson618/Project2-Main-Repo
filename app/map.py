#%%
import plotly.graph_objects as go
import plotly.offline
import pandas as pd
import datetime

#%%
raw_df = pd.read_json(path_or_buf = "http://127.0.0.1:5000/records/", orient="records", convert_dates=True)
raw_df["date"] = raw_df["date"].apply(lambda x: x.strftime('%Y-%m-%d'))
#%%
all_dates = raw_df["date"].unique()
max_date = max(all_dates)

#%%
confirmed_fig = go.Figure()
deaths_fig = go.Figure()
recovered_fig = go.Figure()
#%%
def create_traces(fig, df, confirmed_died_recovered):
    all_dates = df["date"].unique()
    for date in all_dates:
        trace_df = df[df["date"] == date]
        fig.add_trace(
            go.Choropleth(
                locations = trace_df["iso3"],
                z = trace_df[confirmed_died_recovered],
                text = f"{confirmed_died_recovered.title()}",
                autocolorscale=True,
                customdata=[date]  
            ),
        )
create_traces(confirmed_fig, raw_df, "confirmed")
create_traces(deaths_fig, raw_df, "deaths")
create_traces(recovered_fig, raw_df, "recovered")

#%%
def create_slider(fig, most_recent, confirmed_died_recovered):
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[
                # make ith trace visible
                {"visible": [date == i for date in range(len(fig.data))]},
                
                # add title based on trace's metadata
                # {"title.text": f"COVID-19 {confirmed_died_recovered.title()} Cases (as of ({str(fig.data[i].meta["customdata"])}"}
                # META DATA WILL NOT WORK
                ],
        )
        steps.append(step)

    sliders =[
        dict(
            active=len(fig.data)-1,
            currentvalue={"prefix":"Date: "},
            pad = {"t":50},
            steps=steps
        )
    ]

    map_fig.update_layout(
        title={
        'text': f'COVID-19 {confirmed_died_recovered.title()} Cases (as of ({most_recent})',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        sliders=sliders
    )

create_slider(confirmed_fig, max_date, "confirmed")
create_slider(deaths_fig, max_date, "deaths")
create_slider(recovered_fig, max_date, "recovered")



#%%
map_div = plotly.offline.plot(map_fig, include_plotlyjs=False, output_type='div')


# %%
