import numpy as np
import pandas as pd
import sys

from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.layouts import layout, row, widgetbox
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.models.widgets import TextInput, PreText, CheckboxGroup
from bokeh.plotting import figure
from queryYelp import query_api


### configure input widgets ###
term = TextInput(title="Search Term", value='Restaurants')
location = TextInput(title="Location", value='San Francisco')
# num_dollars = CheckboxGroup(labels=["$", "$$", "$$$", "$$$$"], active=[0, 1, 2, 3])
pre = PreText(text="")


### create Column Data Source that will be used by plot ###
source = ColumnDataSource(data=dict(name=[], price=[], rating=[], review_count=[], 
	log_review=[], color=[], size=[], score=[]))


### initialize plot gradients ###
# 10-step 'goodness' gradient from https://uigradients.com/#Nepal
rating_colors = ['#2657EB', '#3858DD','#4A59CF', '#5D5AC1', '#6F5BB3',
		'#945D98','#A65E8A', '#B95F7C', '#CB606E', '#DE6161']
# 5-step price gradient
price_size = [5, 8, 11, 14, 17]


### configure hover tool ###
hover = HoverTool(tooltips=[
    ("Name", "@name"),
    ("Rating", "@rating"),
    ("Price", "@price")
])


### add in page style ###
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)


### set up initial plot ###
p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tools=[hover])
p.circle(x="rating", y="log_review", source=source, size="size", color="color", line_color="color", fill_alpha=0.6)
p.xaxis.axis_label = "Business Rating"
p.yaxis.axis_label = "log10(Number of Reviews)"


### update title ###
def update_title(attrname, old, new):
	cleaned_location = (location.value).split(',')[0]
	plot.title.text = (term.value).title() + " in " + cleaned_location.title()


### run query ###
def select_data():
	## fetch data from initial default query ##
	results = query_api(term.value, location.value)
	restaurant_meta = pd.DataFrame(results, columns=['name', 'price', 'rating', 'review_count'])

	## clean ##
	restaurant_meta.fillna(0, inplace=True)  # replace missing values with zero
	restaurant_meta['price'] = [len(i) for i in (restaurant_meta['price']).astype(str)] # convert price values to ints

	## compute score ##
	# higher score (0-1) is better
	# very simple implementation
	scaled_rating_scaled = [x/max(restaurant_meta['rating']) for x in restaurant_meta['rating']]
	scaled_review_count = [x/max(restaurant_meta['review_count']) for x in restaurant_meta['review_count']]
	restaurant_meta['score'] = [(x+y)/2 for x,y in zip(*[scaled_rating_scaled, scaled_review_count])]
	restaurant_meta = restaurant_meta.sort_values(restaurant_meta.columns[4], ascending = False) # sort by score

	## add in plot color and size ##
	# color based on score (warmer is higher score)
	# size based on price (bigger size is higher price)
	restaurant_meta['color'] = [rating_colors[i] for i in (restaurant_meta['score']/0.1).astype(int)]
	restaurant_meta['size'] = [price_size[i] for i in (restaurant_meta['price']).astype(int)]

	## log10-scale review count ##
	log_review = [np.log10(x) for x in restaurant_meta['review_count']]
	restaurant_meta['log_review'] = log_review

	## change price back to dollar-signs ##
	restaurant_meta['price'] = [("$" * i) for i in (restaurant_meta['price']).astype(int)]

	return restaurant_meta


### update plot ###
def update():
	pre.text = "Loading..."
	init_update()
	pre.text = ""

def init_update():
	df = select_data()
	p.title.text = (term.value).title() + " in " + (location.value).title()
	source.data = dict(
		name=df['name'],
		price=df['price'],
		rating=df['rating'],
		review_count=df['review_count'],
		log_review=df['log_review'],
		color=df['color'],
		size=df['size'],
		score=df['score']
	)

### control page updates ###
controls = [term, location]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

### add to document ###
# 'scale_width' also looks nice with this example
sizing_mode = 'fixed'  
widgets = [term, location, pre]
inputs = widgetbox(*widgets, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

init_update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Yelp Explorer"



