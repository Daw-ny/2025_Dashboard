#######################################################
# packages
from dash import html

#######################################################
# file imports
from pages import home_page, AD, Fog

#######################################################

def render_page_content(pathname):
    if pathname == "/":
        return home_page.layout
    elif pathname == "/Anomaly-Detection":
        return AD.layout
    elif pathname == "/Fog-prediction":
        return Fog.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )