import os
import pandas as pd
import psycopg2
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.express as px

def fetch_data():
    
    conn = psycopg2.connect(
        host=os.environ.get("DATABASE_HOST", "localhost"),
        dbname=os.environ.get("DATABASE_NAME", "mydatabase"),
        user=os.environ.get("DATABASE_USER", "myuser"),
        password=os.environ.get("DATABASE_PASSWORD", "mypassword")
    )
    query = "SELECT * FROM ai_content_impact ORDER BY published_date"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time AI Content Impact Dashboard"),
    dcc.Graph(id="live-chart"),

    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  
        n_intervals=0
    )
])

@app.callback(
    Output("live-chart", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_chart(n):
    df = fetch_data()
    fig = px.line(
        df, 
        x="published_date", 
        y="ai_adoption_rate", 
        color="industry",
        title="AI Adoption Rate Over Time by Industry"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
