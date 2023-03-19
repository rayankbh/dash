
import dash
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
                dcc.Graph(
                    id="deliveries-graph",
                    figure=px.bar(
                        deliveries_df,
                        x="Month",
                        y="Deliveries",
                        title="Monthly Deliveries",
                    ),
                ),
                dcc.Graph(
                    id="volunteers-graph",
                    figure=px.line(
                        volunteers_df,
                        x="Month",
                        y="Volunteers",
                        title="Monthly Volunteers",
                    ),
                ),
                dcc.Graph(
                    id="inventory-graph",
                    figure=px.area(
                        inventory_df,
                        x="Month",
                        y="Inventory",
                        title="Monthly Inventory",
                    ),
                ),
            ],
            className="graphs-container",
        ),
    ],
    className="container",
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
