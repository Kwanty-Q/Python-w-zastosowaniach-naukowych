import numpy as np
from scipy.integrate import odeint, solve_ivp

from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div

beta = 0.5
gamma = 0.5

def func(y, t):
    S, I, R = y
    return -beta*S*I, beta*S*I - gamma*I, gamma*I

S0 = 9
I0 = 1
R0 = 0

ts1 = np.linspace(0, 10, 1000)
res1 = odeint(func, (S0, I0, R0), ts1)

fig = figure(#title = 'Model SIR',
             x_axis_label = 't',
             y_axis_label = 'Liczba osobników',
             width = 400,
             aspect_ratio = 1)
fig.toolbar.logo = None
fig.toolbar.autohide = True
fig.grid.grid_line_dash = (5, 5)

fig.line(ts1, res1[:, 0], color = 'orange', line_width = 3, legend_label = 'S')
fig.line(ts1, res1[:, 1], color = 'cornflowerblue', line_width = 3, legend_label = 'I')
fig.line(ts1, res1[:, 2], color = 'forestgreen', line_width = 3, legend_label = 'R')


# nazwa atrybutu, który został zmieniony; stara wartość; nowa wartość
def callback_beta(attr, old, new):
    beta = new

    fig.renderers = []

    def func(y, t):
        S, I, R = y
        return -beta*S*I, beta*S*I - gamma*I, gamma*I

    ts1 = np.linspace(0, 10, 1000)
    res1 = odeint(func, (S0, I0, R0), ts1)

    fig.line(ts1, res1[:, 0], color = 'orange', line_width = 3, legend_label = 'S')
    fig.line(ts1, res1[:, 1], color = 'cornflowerblue', line_width = 3, legend_label = 'I')
    fig.line(ts1, res1[:, 2], color = 'forestgreen', line_width = 3, legend_label = 'R')

def callback_gamma(attr, old, new):
    gamma = new
    
    fig.renderers = []

    def func(y, t):
        S, I, R = y
        return -beta*S*I, beta*S*I - gamma*I, gamma*I

    ts1 = np.linspace(0, 10, 1000)
    res1 = odeint(func, (S0, I0, R0), ts1)

    fig.line(ts1, res1[:, 0], color = 'orange', line_width = 3, legend_label = 'S')
    fig.line(ts1, res1[:, 1], color = 'cornflowerblue', line_width = 3, legend_label = 'I')
    fig.line(ts1, res1[:, 2], color = 'forestgreen', line_width = 3, legend_label = 'R')




s1 = Slider(start = 0, end = 1, step = 0.01, value = 0.5, title = 'beta', sizing_mode = 'stretch_width')
s2 = Slider(start = 0, end = 1, step = 0.01, value = 0.5, title = 'gamma', sizing_mode = 'stretch_width')
s1.on_change('value_throttled', callback_beta)
s2.on_change('value_throttled', callback_gamma)
# zmiana wartości
# 'value_throttled' - zbiera wartość tylko przy puszczeniu slidera


curdoc().add_root(column(Div(text = 'Model SIR'), row(column(s1, s2, width = 200), fig)))