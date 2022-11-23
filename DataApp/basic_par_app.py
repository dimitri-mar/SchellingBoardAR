import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from skimage import data

img = data.chelsea()
fig = px.imshow(img)
fig.update_layout(
    dragmode="drawrect",
    newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="darkblue", width=8)),
)

app = Dash(__name__)
app.layout = html.Div([dcc.Upload(html.Button('Upload File'), id="upload-img", ),
                       html.Div([

    html.Div(className="break"),
    html.Div(
        [
            html.H3("Drag and draw annotations"),
            dcc.Graph(id="graph-styled-annotations", figure=fig),
            html.Pre('Opacity of annotations'),

        ]
    ), html.Div(
        [
            html.H3("Drag and draw annotations"),
            dcc.Graph(id="graph-styled-annotations", figure=fig),
            html.Pre('Opacity of annotations'),

        ]),html.Div(className="break"),


], style={'display': 'flex', 'flex-direction': 'row'}),
html.Div([dcc.Slider(id="opacity-slider", min=0, max=1, value=0.5,
                                 step=0.1,
                                 tooltip={'always_visible': True}), ])])

@app.callback(
    Output("graph-styled-annotations", "figure"),
    Input("opacity-slider", "value"),
    prevent_initial_call=True,
)
def on_style_change(slider_value, color_value):
    fig = px.imshow(img)
    fig.update_layout(
        dragmode="drawrect",
        newshape=dict(opacity=slider_value, fillcolor=color_value["hex"]),
    )
    return fig

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == "__main__":
    app.run_server(debug=True)
