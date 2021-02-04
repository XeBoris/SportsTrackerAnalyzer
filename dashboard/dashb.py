# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

from sportstrackeranalyzer.module.db_handler import DataBaseHandler
from sportstrackeranalyzer.module.shelve_handler import ShelveHandler


gl_dbh = None
gl_db_user = None
gl_db_type = None
gl_db_path = None
gl_db_name = None
gl_table_org = pd.DataFrame({"row": [1, 2, 3], "row2": [2, 3, 4]})
gl_table_show = None
gl_table_col_show = [{"name": i, "id": i} for i in gl_table_org.columns]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1("Landing page", style={"fontsize": 24}),
        html.Div(
            children=[
                dcc.Input(id='ios-user', type='text',
                          placeholder="koenig",
                          value="koenig"),
                dcc.Input(id='ios-db-type', type='text',
                          placeholder="FileDataBase",
                          value="FileDataBase"),
                dcc.Input(id='ios-db-path', type='text',
                          placeholder="/home/koenig/STAsportsDB",
                          value="/home/koenig/STAsportsDB"),
                dcc.Input(id='ios-db-name', type='text',
                          placeholder="sportsDB",
                          value="sportsDB")
            ]
        ),
        # html.Div(
        #     children=dcc.Input(id='ios-type', type='text')
        # ),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
                 style={'display': 'none'}),
        html.Button('Load Table', id='load-table', n_clicks=0),
        dash_table.DataTable(
            id='table',
            columns=gl_table_col_show,
            data=[],
            selected_rows=[],
            row_selectable="multi",
            style_as_list_view=True,
            style_table={
                'overflowX': 'scroll',
                'width': '1000px',
                'maxHeight': '20ex',
            },
            style_data={
                'width': '100%',
            },
            style_cell={
                'padding': '5px',
                'textAlign': 'left'
                },
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        ),
        html.Div(id='table-row-selected',
                 children="Table"),
        dcc.Graph(figure=None)
    ]
)


@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('ios-user', 'value'),
     State('ios-db-type', 'value'),
     State('ios-db-path', 'value'),
     State('ios-db-name', 'value'),
     ]
)
def update_settings(n_clicks,
                    value_user,
                    value_type,
                    value_path,
                    value_name):
    global gl_db_type, gl_db_name, gl_db_path, gl_db_user, gl_table
    gl_db_user = value_user
    gl_db_type = value_type
    gl_db_path = value_path
    gl_db_name = value_name

    print(gl_db_user, gl_db_type)

    loadDB()

@app.callback(
    [Output('table', 'data'), Output('table', 'columns')],
    [Input('load-table', 'n_clicks')],
)
def load_table(n_clicks):
    global gl_table_org, gl_table_show, gl_table_col_show

    gl_table_org = getUserTracks()
    try:
        gl_table_show = gl_table_org.drop(["created_at", "updated_at", "notes", "leaf",
                  "start_time_timezone_offset", "end_time_timezone_offset",
                  "user_hash"],
                    axis=1)
    except:
        gl_table_show = gl_table_org

    gl_table_col_show = [{"name": i, "id": i} for i in gl_table_show.columns]

    return gl_table_show.to_dict("records"), gl_table_col_show

@app.callback(
    Output('table-row-selected', 'children'),
    [Input('table', 'selected_rows'),
     Input('table', 'derived_virtual_row_ids')]
)
def update_table(selected_rows, derived_virtual_row_ids):
    print(selected_rows)
    sel_dataframe = None
    select_rows_from_dataframe = []
    if len(selected_rows) > 0 and len(selected_rows) <= len(gl_table_show) and 'track_hash' in gl_table_show:
        select_rows_from_dataframe = gl_table_show.loc[selected_rows].track_hash
        sel_dataframe = gl_table_org.loc[gl_table_org['track_hash'].isin(select_rows_from_dataframe)]

        select_rows_from_dataframe = select_rows_from_dataframe.to_list()
        print(sel_dataframe)
        print(select_rows_from_dataframe)

    if len(select_rows_from_dataframe) == 1:
        try:
            k = GetAllLeaves(gl_table_org, select_rows_from_dataframe[0])
            k_gps = k.get("gps")
            print(k_gps.head(3))

            fig = px.scatter_mapbox(k_gps, lat="latitude", lon="longitude", zoom=3)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.show()


        except:
            pass

    return f"Selected Rows: {len(selected_rows)} with track hash:"


def loadDB():
    global gl_dbh
    gl_dbh = DataBaseHandler(db_type=gl_db_type)
    gl_dbh.set_db_path(db_path=gl_db_path)
    gl_dbh.set_db_name(db_name=gl_db_name)

    db_exists = gl_dbh.get_database_exists()
    print(db_exists)

def getUserTracks():

    global gl_db_user
    if gl_db_user is None:
        return gl_table_org

    user_entry = gl_dbh.search_user(user=gl_db_user, by="username")

    user_hash = user_entry[0].get("user_hash")

    user_tracks = gl_dbh.read_branch(key="user_hash", attribute=user_hash)

    df = pd.DataFrame(user_tracks)
    df["start_time"] = pd.to_datetime(df["start_time"], unit="ms")
    df["end_time"] = pd.to_datetime(df["end_time"], unit="ms")
    df["created_at"] = pd.to_datetime(df["created_at"], unit="ms")
    df["updated_at"] = pd.to_datetime(df["updated_at"], unit="ms")

    return df



#later export
def GetLeafNames(df, hashi):
    df0 = df[df["track_hash"] == hashi]
    try:
        df_leafs = pd.json_normalize(df0["leaf"])
        leaf_names = [i.split(".")[0] for i in df_leafs.keys()]
        leaf_names = list(set(leaf_names))
        return leaf_names
    except:
        return []


def GetLeaf(df, hashi, leaf_name):
    df0 = df[df["track_hash"] == hashi]
    df_leafs = pd.json_normalize(df0["leaf"])

    result = df_leafs.to_json(orient="records")
    result = json.loads(result)

    leaf_name = result[0][f"{leaf_name}.name"]
    leaf_hash = result[0][f"{leaf_name}.leaf_hash"]

    return leaf_name, leaf_hash


def GetTrack(df, hashi):
    df0 = df[df["track_hash"] == hashi]
    result = df0.to_json(orient="records")

    return json.loads(result)


def GetAllLeaves(df, hashi):
    all_leaves = GetLeafNames(df, hashi)

    leaf_content_dict = {}

    for i_leaf in all_leaves:
        leaf_name, leaf_content = GetLeaf(df, hashi, i_leaf)

        df_i = gl_dbh.read_leaf(directory=leaf_name,
                             leaf_hash=leaf_content,
                             leaf_type="DataFrame")

        leaf_content_dict[i_leaf] = df_i

    return leaf_content_dict





if __name__ == '__main__':
    app.run_server(debug=True)
