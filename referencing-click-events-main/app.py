import pandas as pd
import dash 
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform


app = DashProxy(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[MultiplexerTransform(proxy_location=None)])


df = pd.read_excel('sampleDF.xlsx')

# print(df.info())

fig_3d = px.scatter_3d(df, x='x', y='y', z='z',
              color='k', size_max=18,
              opacity=0.7)
fig_3d.update_layout(
    title='3-D Scatter Plot'
)


app.layout = dbc.Container(
                            [
                                dbc.Row(
                                    [
                                    html.H1(['Referencing Click Events between graphs'],style={'text-align':'center'}),
                                    html.Hr(style={'background-color':'rgba(61,61,61,0.5)'}),
                                    ],style={'margin-top':'10px', 'height' : '10vh'}
                                ),
                                dbc.Row(
                                        [
                                            dbc.Col(id='col-1',
                                                    children=[
                                                        dcc.RangeSlider(
                                                            id='slider',
                                                            min=df['time'].dt.year.min(),
                                                            max=df['time'].dt.year.max(),
                                                            # step=df['time'].dt.year,
                                                            value=[0, df['time'].dt.year.nunique()-1],
                                                            allowCross=False,
                                                            updatemode='mouseup',
                                                            tooltip={'always_visible': True, 'placement': 'bottom'},
                                                            ),
                                                        dcc.Graph(id='3d-scatter',figure=fig_3d, style = {'height' : '100vh', 'margin-top' : '120px'})
                                                    ]
                                                ),
                                            dbc.Col(id='col-2',
                                                    children=[
                                                        dbc.Label('Select Field'),
                                                        dcc.Dropdown(['a','b','c'], 'a', id='dropdown', style={'height' : '5vh'}),
                                                        dcc.Graph(id='line-plot', style={'height' : '60vh'}),
                                                        dbc.Row([
                                                        dbc.Col(id='col-3',
                                                            children=[
                                                                dbc.Label('Select Field'),
                                                                dcc.Dropdown(['a','b','c'], 'b', id='dropdown-2', style={'height' : '5vh'}),
                                                                dcc.Graph(id='line-plot-2', style={'height' : '60vh'})
                                                    ]
                                                )
                                            ])
                                                    ]),
                                           
                                        ], style = {'height' : '80vh'}
                                    )
                            ],fluid=True, style={'height' : '100vh'}
    )



@app.callback(
              Output('line-plot', 'figure'),
              [Input('3d-scatter','clickData'),Input('dropdown','value')]
)
def click_data(data,value):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    line_fig = px.line(df,x='time',y=value)
    line_fig.update_layout(
        title='Line Plot',
        margin=dict(l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"
    )
    
    line_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(61,61,61,0.5)',showgrid=False,zeroline=False)
    line_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(61,61,61,0.5)',showgrid=False,zeroline=False)

    if button_id == "dropdown":
        return line_fig
    elif button_id == "3d-scatter":
        selected_point = data['points'][0]
        line_fig.add_trace(go.Scatter(x=[df['time'][selected_point['pointNumber']]], y=[df[value][selected_point['pointNumber']]], mode = 'markers',
                         marker_size = 20))
        line_fig.add_annotation(
            xref='x',
            yref='y',
            arrowhead=2,
            ax=0,
            ay=-100,
            x=df['time'][selected_point['pointNumber']],
            y=df[value][selected_point['pointNumber']],
            text="An annotation referencing point from 3-D scatter plot"
        )
        line_fig.update_layout(showlegend=False)
        
    
    
        return line_fig       
    else:
        return line_fig      


@app.callback(
              Output('line-plot-2', 'figure'),
              [Input('3d-scatter','clickData'),Input('dropdown-2','value')]
)
def click_data_2(data,value):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    line_fig = px.line(df,x='time',y=value)
    line_fig.update_layout(
        title='Line Plot',
        margin=dict(l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"
    )
    
    line_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(61,61,61,0.5)',showgrid=False,zeroline=False)
    line_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(61,61,61,0.5)',showgrid=False,zeroline=False)

    if button_id == "dropdown-2":
        return line_fig
    elif button_id == "3d-scatter":
        selected_point = data['points'][0]
        line_fig.add_trace(go.Scatter(x=[df['time'][selected_point['pointNumber']]], y=[df[value][selected_point['pointNumber']]], mode = 'markers',
                         marker_size = 20))
        line_fig.add_annotation(
            xref='x',
            yref='y',
            arrowhead=2,
            ax=0,
            ay=-100,
            x=df['time'][selected_point['pointNumber']],
            y=df[value][selected_point['pointNumber']],
            text="An annotation referencing point from 3-D scatter plot"
        )
        line_fig.update_layout(showlegend=False)
        
    
    
        return line_fig       
    else:
        return line_fig 


# @app.callback(
#               Output('line-plot', 'figure'),
#               [Input('slider','value'),
#               Input('line-plot','value')]
# )
# def update_line_plot(years, value):
    
#     dff = df.loc[years[1]:years[0]]

#     fig = px.line(dff, x='time', y=value)

#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)