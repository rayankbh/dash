import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Load data
deliveries_df = pd.read_csv("deliveries.csv")
volunteers_df = pd.read_csv("volunteers.csv")
inventory_df = pd.read_csv("inventory.csv")

# Create the app
app = dash.Dash(__name__)
server = app.server

# Define the layout
app.layout = html.Div(
    [
        html.H1("Delivery Progress Dashboard"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Deliveries"),
                        html.H4(f"{deliveries_df['Deliveries'].sum()} Total Deliveries"),
                    ],
                    className="metric",
                ),
                html.Div(
                    [
                        html.H3("Volunteers"),
                        html.H4(f"{volunteers_df['Volunteers'].sum()} Total Volunteers"),
                    ],
                    className="metric",
                ),
                html.Div(
                    [
                        html.H3("Inventory"),
                        html.H4(f"{inventory_df['Inventory'].sum()} Total Inventory"),
                    ],
                    className="metric",
                ),
            ],
            className="metrics-container",
        ),
        html.Div(
            [
                html.H2("Data Table"),
                html.Table(
                    [
                        html.Thead(
                            html.Tr([html.Th(col) for col in deliveries_df.columns])
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [html.Td(deliveries_df.iloc[i][col]) for col in deliveries_df.columns]
                                )
                                for i in range(len(deliveries_df))
                            ]
                        ),
                    ]
                ),
            ],
            className="data-container",
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="filter-dropdown",
                    options=[{"label": col, "value": col} for col in deliveries_df.columns],
                    value="Month",
                    clearable=False,
                ),
                dcc.Graph(id="deliveries-graph"),
                dcc.Graph(id="volunteers-graph"),
                dcc.Graph(id="inventory-graph"),
            ],
            className="graphs-container",
        ),
    ],
    className="container",
)

# Add authentication
VALID_USERNAME_PASSWORD_PAIRS = {
    "admin": "password"
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Define callbacks
@app.callback(
    [
        dash.dependencies.Output("deliveries-graph", "figure"),
        dash.dependencies.Output("volunteers-graph", "figure"),
        dash.dependencies.Output("inventory-graph", "figure"),
    ],
    [dash.dependencies.Input("filter-dropdown", "value")],
)
def update_graphs(filter_col):
    fig_deliveries = px.bar(
        deliveries_df,
        x=filter_col,
        y="Deliveries",
        title="Monthly Deliveries",
    )
    fig_volunteers = px.line(
        volunteers_df,
        x=filter_col,
        y="Volunteers",
        title="Monthly Volunteers",
    )
    fig_inventory = px.area(
        inventory_df,
        x=filter_col,
        y="Inventory",
        title="Monthly Inventory",
    )
    return fig_deliveries, fig_volunteers, fig_inventory

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
