from bokeh.client import push_session
# from bokeh.embed import server_document
from bokeh.embed import autoload_server
from bokeh.plotting import figure, curdoc

plot = figure()
plot.circle([1,2], [3,4])

doc = curdoc()
doc.add_root(plot)

script = autoload_server(app_path="animate") # note the app path
print(script)