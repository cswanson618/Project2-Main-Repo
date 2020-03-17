// TIMESERIES PLOT

var trace1 = {
  type: "scatter",
  mode: "lines",
  name: 'Confirmed Cases',
  x: db.date
  y: db.confirmed,
  line: {color: '#17BECF'}
}

var trace2 = {
  type: "scatter",
  mode: "lines",
  name: 'Deaths Cases',
  x: db.date
  y: db.deaths,
  line: {color: '#7F7F7F'}
}

var data = [trace1,trace2];

var layout = {
  title: 'Covid -1 9',
};

Plotly.newPlot('myDiv', data, layout);
})