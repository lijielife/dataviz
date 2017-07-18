import numpy as np
import sys

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Button
from bokeh.models.widgets import Select,Slider, TextInput
from bokeh.plotting import figure

from queryYelp import query_api

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 5], y_range=[0, 1000])

# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
term = TextInput(title="term", value='restaurants')
location = TextInput(title="location", value='San Francisco, CA')

text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1)
button = Button(label="Press Me")

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = term.value + " in " + location.value

def call_query():
	print("in callback")
	query_api("restaurants", "95148")

text.on_change('value', update_title)
ratings, num_reviews = query_api("restaurants", "95148")

xval = list(ratings.values())
yval = list(num_reviews.values())

# for r in range(0, len(ratings.values())):
# 	xval = xval + r


# for n in range(0, len(num_reviews.values())):
# 	yval = yval + n

plot.circle(xval, yval, line_width=2,size = 5)
# plot.line(ratings.values(), num_reviews.values())

# button.on_click(call_query())

# term.on_change('value', query_api("restaurants", "95148"))
# location.on_change('value', query_api("restaurants", "95148"))
# location.on_change('value', query_api(str(term), str(location)))

def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(term, location, button, text, offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"