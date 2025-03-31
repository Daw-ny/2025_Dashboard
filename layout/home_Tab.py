#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html
#######################################################
# file imports
from style.hometabstyle import HOMETAB
#######################################################
card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Explain", tab_id="tab-1", active_label_style=HOMETAB),
                    dbc.Tab(label="AD", tab_id="tab-2", active_label_style=HOMETAB),
                    dbc.Tab(label="FOG", tab_id="tab-3", active_label_style=HOMETAB),
                    dbc.Tab(label="Manitto", tab_id="tab-4", active_label_style=HOMETAB),
                    dbc.Tab(label="Liver", tab_id="tab-5", active_label_style=HOMETAB),
                    dbc.Tab(label="Pregnant", tab_id="tab-6", active_label_style=HOMETAB),
                ],
                id="card-tabs",
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(
            html.P(id="card-content", className="card-text")
        ),
    ]
)
