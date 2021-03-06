
import pandas as pd
import numpy as np


import plotly.offline as py
import plotly.graph_objs as go


# Look at 1 player over time
player_id = "00-0020531"
brees = player_ppg[player_ppg.player_id == player_id].sort_values('date_time')

# Get lines for each season
data = []
for yr in brees.season_year.unique():
    that_year = brees[(brees.season_type == 'Regular') & (brees.season_year == yr)]
    data.append(
            go.Scatter(
                    x = that_year['week'],
                    y = that_year['total_points'],
                    name = str(yr)
                )
        )
# Define graph features
layout = go.Layout(
    title='Drew Brees Fantasy points',
    yaxis=dict(title='Point per Game'),
    xaxis=dict(title='Week of Season')
)

# Build figure
fig = go.Figure(data=data, layout=layout)
py.plot(fig)



## Top 10 QB's in 2017
keep_rows = (player_ppg.position == 'QB') & (player_ppg.season_year == 2017) & (player_ppg.season_type == 'Regular')
top10_players = player_ppg[keep_rows] \
    .groupby('full_name') \
    .agg({'total_points':np.mean}) \
    .sort_values('total_points',ascending=False) \
    .head(10).index.values



data = []
for player_name in top10_players:
    line_df = player_ppg[keep_rows & (player_ppg.full_name == player_name)]
    data.append(
            go.Scatter(
                    x = line_df['week'],
                    y = line_df['total_points'],
                    name = player_name
                )
        )
# Define graph features
layout = go.Layout(
    title='2017 Regular Season Top 10 QBs',
    yaxis=dict(title='Point per Game'),
    xaxis=dict(title='Week of Season')
)

# Build figure
fig = go.Figure(data=data, layout=layout)
py.plot(fig)


## QB score density plot
go.



