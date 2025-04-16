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
    # Ensure published_date is a datetime
    df['published_date'] = pd.to_datetime(df['published_date'])
    conn.close()
    return df

app = Dash(__name__)

# Get initial data to determine slider range. This is only done once on app load.
df_initial = fetch_data()
# Extract unique years from published_date column
years = df_initial['published_date'].dt.year.unique().tolist()
min_year = int(min(years))
max_year = int(max(years))

app.layout = html.Div([
    html.H1("Real-Time AI Content Impact Dashboard", style={'textAlign': 'center'}),
    html.H3("AI Adoption Rate Over Time by Industry", style={'textAlign': 'center'}),
    
    # Year slider for filtering data dynamically
    html.Div([
        dcc.Slider(
            id='year-slider',
            min=min_year,
            max=max_year,
            value=max_year,
            marks={str(year): str(year) for year in range(min_year, max_year + 1)},
            step=None
        )
    ], style={'width': '80%', 'padding': '20px', 'margin': 'auto'}),
    
    dcc.Graph(id="live-chart"),
    
    # Real-time interval update (every 5 seconds)
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  
        n_intervals=0
    )
])

@app.callback(
    Output("live-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("year-slider", "value")]
)
def update_chart(n_intervals, selected_year):
    df = fetch_data()
    # Filter data: display only records where the year is less than or equal to the selected year.
    df = df[df['published_date'].dt.year <= selected_year]
    
    # Create a line chart with markers and improved color palette
    fig = px.line(
        df,
        x="published_date",
        y="ai_adoption_rate",
        color="industry",
        markers=True,
        line_shape='linear',
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"AI Adoption Rate Over Time by Industry (up to {selected_year})"
    )
    
    # Update layout for better readability
    fig.update_layout(
        hovermode='x unified',
        legend_title_text='Industry',
        template='plotly_white',
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

if __name__ == '__main__':
    # Run on all interfaces so that Docker port mapping works
    app.run(debug=True, host='0.0.0.0', port=8050)
