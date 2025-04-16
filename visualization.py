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
    df['published_date'] = pd.to_datetime(df['published_date'])
    conn.close()
    return df

def aggregate_data(df, column):
   
    df['year'] = df['published_date'].dt.year
    df_grouped = df.groupby(['industry', 'year'], as_index=False).agg({
        column: 'mean'
    })
    df_grouped['published_date'] = pd.to_datetime(df_grouped['year'], format='%Y')
    return df_grouped


app = Dash(__name__)
server = app.server  


df_initial = fetch_data()

df_agg_initial = aggregate_data(df_initial, 'ai_adoption_rate')
years = df_agg_initial['year'].unique().tolist()
min_year = int(min(years))
max_year = int(max(years))

app.layout = html.Div([
    html.H1("Real-Time AI Content Impact Dashboard", style={'textAlign': 'center'}),
    html.H3("AI Adoption and Job Loss Trends Over Time by Industry", style={'textAlign': 'center'}),
    

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
    

    dcc.Graph(id="jobloss-chart"),
    

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
def update_adoption_chart(n_intervals, selected_year):
    df = fetch_data()
    df_agg = aggregate_data(df, 'ai_adoption_rate')

    df_filtered = df_agg[df_agg['year'] <= selected_year]

    fig = px.line(
        df_filtered,
        x="published_date",
        y="ai_adoption_rate",
        color="industry",
        markers=True,
        line_shape='linear',
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"AI Adoption Rate Over Time by Industry (up to {selected_year})"
    )
    
    fig.update_layout(
        hovermode='x unified',
        legend_title_text='Industry',
        template='plotly_white',
        margin=dict(l=40, r=40, t=80, b=40),
        height=700
    )

    fig.update_yaxes(title_text="AI Adoption Rate (%)", ticksuffix="%")

    return fig


@app.callback(
    Output("jobloss-chart", "figure"),
    [Input("interval-component", "n_intervals"),
     Input("year-slider", "value")]
)
def update_jobloss_chart(n_intervals, selected_year):
    df = fetch_data()
    df_agg = aggregate_data(df, 'job_loss_due_to_ai')
  
    df_filtered = df_agg[df_agg['year'] <= selected_year]

    fig = px.line(
        df_filtered,
        x="published_date",
        y="job_loss_due_to_ai",
        color="industry",
        markers=True,
        line_shape='linear',
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"Job Loss Due to AI Over Time by Industry (up to {selected_year})"
    )
    
    fig.update_layout(
        hovermode='x unified',
        legend_title_text='Industry',
        template='plotly_white',
        margin=dict(l=40, r=40, t=80, b=40),
        height=700
    )

    fig.update_yaxes(title_text="Job Loss Due to AI (%)", ticksuffix="%")

    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
