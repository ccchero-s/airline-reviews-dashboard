from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.graph_objects as go

reviews = pd.read_csv('airlines_reviews.csv')
reviews['Review Date'] = pd.to_datetime(reviews['Review Date'])

airline_websites = {
    'All Nippon Airways': 'https://www.ana.co.jp/en/au/',
    'Air France': 'https://wwws.airfrance.com.au/',
    'Cathay Pacific': 'https://www.cathaypacific.com/cx/en_AU.html',
    'Emirates': 'https://www.emirates.com/au/english/',
    'EVA Air': 'https://www.evaair.com/en-gb/index.html',
    'Japan Airlines': 'https://www.jal.co.jp/au/en/',
    'Korean Air': 'https://www.koreanair.com',
    'Qatar Airways': 'https://www.qatarairways.com/en-au/homepage.html',
    'Singapore Airlines': 'https://www.singaporeair.com',
    'Turkish Airlines': 'https://www.turkishairlines.com'
}

search_data = reviews[
    ['Airline', 'Seat Comfort', 'Staff Service', 'Food & Beverages',
     'Inflight Entertainment', 'Value For Money', 'Overall Rating', 'Recommended']
]

app = Dash(__name__)

years = sorted(reviews['Review Date'].dt.year.unique())
months = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
classes = reviews['Class'].unique()

app.layout = html.Div(style={'width': '100%', 'height': '100vh', 'overflow': 'hidden'}, children=[
    html.Div([
        html.H1(
            "Airline Reviews Dashboard",
            style={
                'textAlign': 'center',
                'marginTop': '20px',
                'marginBottom': '20px',
                'backgroundColor': '#ADD8E6',
                'color': 'white',
                'padding': '20px',
                'borderRadius': '20px',
                'fontSize': '36px'
            }
        )
    ], style={'width': '100%', 'textAlign': 'center'}),

    html.Div(style={'display': 'flex', 'height': 'calc(100vh - 120px)', 'overflow': 'hidden'}, children=[
        html.Div(style={
            'flex': '0 0 300px',
            'padding': '20px',
            'border': '1px solid #ddd',
            'borderRadius': '5px',
            'backgroundColor': '#f9f9f9',
            'overflowY': 'auto'
        }, children=[
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[
                html.Div([
                    html.Label("Start Year", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='start-year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in years],
                        value=years[0],
                        clearable=False
                    )
                ], style={'flex': '1', 'marginRight': '10px'}),

                html.Div([
                    html.Label("End Year", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='end-year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in years],
                        value=years[-1],
                        clearable=False
                    )
                ], style={'flex': '1'})
            ]),

            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '10px'}, children=[
                html.Div([
                    html.Label("Start Month", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='start-month-dropdown',
                        options=[{'label': months[m], 'value': m} for m in months],
                        value=1,
                        clearable=False
                    )
                ], style={'flex': '1', 'marginRight': '10px'}),

                html.Div([
                    html.Label("End Month", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='end-month-dropdown',
                        options=[{'label': months[m], 'value': m} for m in months],
                        value=12,
                        clearable=False
                    )
                ], style={'flex': '1'})
            ]),

            html.Label("Class", style={'fontWeight': 'bold', 'marginTop': '10px'}),
            dcc.RadioItems(
                id='class-radio',
                options=[{'label': cls, 'value': cls} for cls in classes],
                value=classes[0],
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            ),

            html.Div(id='filtered-results', style={'marginTop': '20px', 'height': '400px', 'overflowY': 'auto'})
        ]),

        html.Div(style={'flex': '1', 'height': 'calc(100vh - 120px)', 'overflowY': 'auto'}, children=[
            html.Div(style={'display': 'flex', 'width': '100%'}, children=[
                html.Div([
                    dcc.Dropdown(
                        id='airline-dropdown',
                        options=[{'label': airline, 'value': url} for airline, url in airline_websites.items()],
                        placeholder="Select an airline",
                        style={'width': '100%', 'marginTop': '40px'}
                    ),
                    html.Div(id='website-link', style={'marginTop': '20px'})
                ], style={'flex': '1', 'padding': '10px'}),

                html.Div([
                    dcc.Graph(id='gauge-chart', style={'height': '300px', 'width': '400px'})
                ], style={'flex': '1', 'padding': '10px'})
            ]),

            html.H2("Satisfaction Rating", style={'textAlign': 'left', 'paddingLeft': '10px', 'marginTop': '0px'}),

            html.Div([
                dash_table.DataTable(
                    id="data-table",
                    columns=[{"name": col, "id": col} for col in search_data.columns],
                    data=[],
                    page_size=5,
                    sort_action="native",
                    sort_by=[{'column_id': 'Overall Rating', 'direction': 'asc'}],
                    style_table={
                        'overflowX': 'auto',
                        'maxHeight': '400px',
                        'overflowY': 'auto',
                        'border': '1px solid #ddd'
                    },
                    style_cell={
                        'fontSize': '12px',
                        'padding': '5px',
                        'textAlign': 'left'
                    }
                )
            ], style={'width': '100%', 'padding': '10px'}),

            html.Div([
                html.H2(
                    "Average Ratings by Traveler Type and Airline",
                    style={'textAlign': 'left', 'paddingLeft': '10px', 'fontSize': '24px', 'margin': '5px 0'}
                ),
                dcc.Graph(id='heatmap')
            ], style={'padding': '20px'})
        ])
    ])
])

@app.callback(
    [
        Output('website-link', 'children'),
        Output('gauge-chart', 'figure'),
        Output('filtered-results', 'children'),
        Output('data-table', 'data'),
        Output('heatmap', 'figure')
    ],
    [
        Input('start-year-dropdown', 'value'),
        Input('start-month-dropdown', 'value'),
        Input('end-year-dropdown', 'value'),
        Input('end-month-dropdown', 'value'),
        Input('class-radio', 'value'),
        Input('data-table', 'sort_by'),
        Input('airline-dropdown', 'value')
    ]
)
def update_content(start_year, start_month, end_year, end_month, selected_class, sort_by, selected_website):
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=28) + pd.offsets.MonthEnd(0)

    filtered_reviews = reviews[
        (reviews['Review Date'] >= start_date) &
        (reviews['Review Date'] <= end_date) &
        (reviews['Class'] == selected_class)
    ].copy()

    if sort_by:
        sort_column = sort_by[0]['column_id']
        sort_direction = sort_by[0]['direction']
        filtered_reviews = filtered_reviews.sort_values(by=sort_column, ascending=(sort_direction == 'asc'))

    reviews_display = [
        html.Div([
            html.H3(row['Title'], style={'color': '#007bff', 'fontWeight': 'bold'}),
            html.P(f"Name: {row['Name']}"),
            html.P(f"Review Date: {row['Review Date'].strftime('%Y-%m-%d')}"),
            html.P(f"Month Flown: {row['Month Flown']}"),
            html.P(f"Class: {row['Class']}"),
            html.P(f"Review: {row['Reviews']}", style={'lineHeight': '1.5'})
        ], style={'border': '1px solid #ddd', 'padding': '10px', 'marginBottom': '10px'})
        for _, row in filtered_reviews.iterrows()
    ]

    website_link = (
        html.A('Go to airline website', href=selected_website, target="_blank")
        if selected_website else "Please select an airline."
    )

    filtered_reviews['Recommended'] = (
        filtered_reviews['Recommended']
        .astype(str)
        .str.strip()
        .str.title()
        .map({'Yes': 1, 'No': 0})
    )

    if len(filtered_reviews) > 0 and filtered_reviews['Recommended'].notnull().sum() > 0:
        recommendation_rate = (filtered_reviews['Recommended'].sum() / len(filtered_reviews)) * 100
    else:
        recommendation_rate = 0

    gauge_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=recommendation_rate,
        title={'text': "Recommendation Rate"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"}
        }
    ))

    data = filtered_reviews.to_dict('records')

    heatmap_data = filtered_reviews.groupby(['Type of Traveller', 'Airline']).agg(
        avg_rating=('Overall Rating', 'mean')
    ).round(2).reset_index()

    heatmap_pivot = heatmap_data.pivot(index='Type of Traveller', columns='Airline', values='avg_rating')

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        texttemplate="%{z:.2f}",
        colorscale='Blues',
        colorbar=dict(title='Avg Rating')
    ))

    fig.update_layout(
        xaxis_title="Airline",
        yaxis_title="Type of Traveller"
    )

    return website_link, gauge_figure, reviews_display, data, fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
