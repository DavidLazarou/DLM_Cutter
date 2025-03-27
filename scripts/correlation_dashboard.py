import os
import psycopg2
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from dash import Dash, dcc, html, Input, Output

# Load environment variables
load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Connect to Postgres
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DATABASE
)

# Create the Dash app
app = Dash(__name__)
app.title = "Rolling Correlation Dashboard"

# App layout
app.layout = html.Div([
    html.H2("📈 Rolling Correlation Dashboard"),

    html.Div([
        html.Label("Enter Ticker 1:"),
        dcc.Input(id="ticker1", type="text", value="AAPL", debounce=True),
    ], style={"display": "inline-block", "margin": "10px"}),

    html.Div([
        html.Label("Enter Ticker 2:"),
        dcc.Input(id="ticker2", type="text", value="MSFT", debounce=True),
    ], style={"display": "inline-block", "margin": "10px"}),

    html.Div([
        html.Label("Window Size:"),
        dcc.Dropdown(
            id="window-size",
            options=[{"label": w, "value": w} for w in [20, 30, 60, 90]],
            value=30,
            clearable=False
        ),
    ], style={"display": "inline-block", "margin": "10px"}),

    html.Br(),
    dcc.Graph(id="correlation-graph")
])


# Callback to update the graph
@app.callback(
    Output("correlation-graph", "figure"),
    Input("ticker1", "value"),
    Input("ticker2", "value"),
    Input("window-size", "value")
)
def update_graph(ticker1, ticker2, window):
    query = """
        SELECT date, correlation
        FROM rolling_correlations
        WHERE (
            (ticker1 = %s AND ticker2 = %s)
            OR (ticker1 = %s AND ticker2 = %s)
        ) AND window_size = %s
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(ticker1, ticker2, ticker2, ticker1, window))

    if df.empty:
        fig = px.line(title="No correlation data available for selected tickers and window.")
    else:
        fig = px.line(df, x="date", y="correlation",
                      title=f"Rolling Correlation ({window}-day): {ticker1} vs {ticker2}")
        fig.update_layout(yaxis_title="Correlation", xaxis_title="Date")

    return fig


# Run app
if __name__ == "__main__":
    app.run(debug=True, port=8050)
