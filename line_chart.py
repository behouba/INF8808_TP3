'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.graph_objects as go
import plotly.express as px
import hover_template

from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        dragmode=False,
        annotations=[dict(
            text='No data to display. Select a cell<br>in the heatmap for more information.',
            xref='paper', yref='paper',
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14)
        )]
    )
    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    fig.add_shape(
        type='rect',
        xref='paper', yref='paper',
        x0=0, x1=1,
        y0=0.25, y1=0.75,
        fillcolor=THEME['pale_color'],
        line=dict(width=0),
        layer='below'
    )


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    fig = px.line(line_data, x='Date_Plantation', y='Counts')

    if len(line_data) == 1:
        fig.update_traces(mode='markers')

    fig.update_traces(
        line=dict(color=THEME['line_chart_color']),
        marker=dict(color=THEME['line_chart_color']),
        hovertemplate=hover_template.get_linechart_hover_template()
    )

    fig.update_layout(
        title=f'Trees planted in {arrond} in {year}',
        yaxis_title='Trees',
        xaxis_tickformat='%d %b',
        dragmode=False
    )

    return fig
