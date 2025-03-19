import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load dataset
df = pd.read_csv("data/raw/df_5.csv")
print(df.columns)
df.columns = df.columns.str.replace(r'\xad', '', regex=True)  # Removes soft hyphen
df.rename(columns={'codename': 'codename'}, inplace=True)  # Rename properly with capitalized format


# Rename column 'Release' to 'Launch Year' if it exists
if 'Release' in df.columns:
    df.rename(columns={'Release': 'Launch Year'}, inplace=True)

# Extract year from 'Launch Year' (format: 'Q1 2021')
df['Launch Year (Year Only)'] = df['Launch Year'].str.extract(r'(\d{4})')
df['Launch Year (Year Only)'] = df['Launch Year (Year Only)'].astype(float)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with sidebar for filters
app.layout = html.Div(style={'backgroundColor': '#0071C5', 'height': '100vh', 'padding': '20px'}, children=[

    # Header with Intel logo and title
    html.Div([
        html.Img(src='/assets/intc.png', style={'width': '120px', 'height': 'auto', 'margin-right': '20px'}),
        html.H1("Intel Processor Dashboard", style={'color': 'white', 'margin': '0', 'flex': '1'}),
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/c/c9/Intel-logo.png',
                 style={'width': '120px', 'height': 'auto', 'margin-left': '20px'})
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Main content layout (Filters on left, Graphs on right)
    html.Div([
        
        # Left Panel - Filters
        html.Div(style={'width': '25%', 'padding': '20px'}, children=[

            html.Div([
                html.Label("Select Intel Series:", style={'color': 'white'}),
                dcc.Dropdown(
                    id='series-dropdown',
                    options=[{'label': series, 'value': series} for series in df['Series'].unique()],
                    multi=True,
                    placeholder="Select Intel Series"
                )
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Launch Year Range:", style={'color': 'white'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=int(df['Launch Year (Year Only)'].min()),
                    max=int(df['Launch Year (Year Only)'].max()),
                    value=[int(df['Launch Year (Year Only)'].min()), int(df['Launch Year (Year Only)'].max())],
                    marks={str(year): {'label': str(year), 'style': {'color': 'black', 'font-size': '16px'}} 
                           for year in range(int(df['Launch Year (Year Only)'].min()), int(df['Launch Year (Year Only)'].max()) + 1, 2)},
                    step=1
                )
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Cache (MB):", style={'color': 'white'}),
                dcc.RangeSlider(
                    id='cache-slider',
                    min=df['Cache'].min(),
                    max=df['Cache'].max(),
                    value=[df['Cache'].min(), df['Cache'].max()],
                    marks={str(cache): str(cache) for cache in range(int(df['Cache'].min()), int(df['Cache'].max()) + 2, 2)},
                    step=1
                )
            ], style={'margin-bottom': '20px'}),

            html.Div([
                html.Label("Select Codename:", style={'color': 'white'}),
                dcc.Dropdown(
                    id='codename-dropdown',
                    options=[{'label': codename, 'value': codename} for codename in df['codename'].dropna().unique()],
                    multi=True,
                    placeholder="Select Codename"
                )
            ], style={'margin-bottom': '20px'}),

        ]),

        # Right Panel - Graphs
        html.Div(style={'width': '70%', 'padding': '20px'}, children=[
            dcc.Graph(id='price-trend-graph'),
            dcc.Graph(id='price-comparison-graph'),
            dcc.Graph(id='price-bar-graph'),
            dcc.Graph(id='performance-trend-graph')
        ])

    ], style={'display': 'flex', 'justify-content': 'space-between'})

])


# Callback to update graphs based on filters
@app.callback(
    [
        Output('price-trend-graph', 'figure'),
        Output('price-comparison-graph', 'figure'),
        Output('price-bar-graph', 'figure'),
        Output('performance-trend-graph', 'figure')
    ],
    [
        Input('series-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('cache-slider', 'value'),
        Input('codename-dropdown', 'value')
    ]
)
def update_graphs(selected_series, year_range, selected_cache, selected_codename):
    # Ensure selected_series is not None
    if not selected_series:
        selected_series = df['Series'].unique()

    # Ensure selected_codename is not None
    if not selected_codename:
        selected_codename = df['codename'].dropna().unique()

    # Filter dataframe based on selections
    filtered_df = df[
        (df["Series"].isin(selected_series)) &
        (df["Launch Year (Year Only)"] >= year_range[0]) &
        (df["Launch Year (Year Only)"] <= year_range[1]) &
        (df["Cache"] >= selected_cache[0]) & (df["Cache"] <= selected_cache[1]) &
        (df["codename"].isin(selected_codename))
    ]

    # Sort by Launch Year for proper line plotting
    filtered_df = filtered_df.sort_values(by="Launch Year (Year Only)")

    # Price trends over time (Line Graph)
    fig1 = px.line(filtered_df, x="Launch Year (Year Only)", y="Price ($)", color="Series",
                    title="Price Trends Over Time", markers=True)
    fig1.update_traces(marker=dict(size=8))
    fig1.update_layout(yaxis=dict(autorange="reversed"))

    # Price comparison by series (Box Plot)
    fig2 = px.box(filtered_df, x="Series", y="Price ($)", title="Intel Series Price Comparison")
    fig2.update_layout(yaxis=dict(autorange="reversed"))

    # Price bar graph by year
    fig3 = px.bar(filtered_df, x="Launch Year (Year Only)", y="Price ($)", color="Series",
                   title="Price Over Years")
    fig3.update_layout(yaxis=dict(autorange="reversed"))

    # Processor vs Performance line graph
    fig4 = px.line(filtered_df, x="Launch Year (Year Only)", y="Clock rate (GHz)", color="Series",
                   title="Processor Performance Over Time", markers=True)
    fig4.update_traces(marker=dict(size=8))

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True)
