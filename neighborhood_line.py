import pandas as pd
import bokeh.charts as charts
from bokeh.models.widgets import Select
from bokeh.io import output_file, show, vform
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm
from bokeh.io import curdoc

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

# load data
df = pd.read_csv('data/sf_listings.csv', parse_dates=['last_review'], infer_datetime_format=True).set_index('id')
df_reviews = pd.read_csv('data/reviews.csv', parse_dates=['date'], infer_datetime_format=True).set_index('listing_id')
review_timeseries = df.join(df_reviews)
reviews = pd.crosstab(review_timeseries.date, review_timeseries.neighbourhood).resample('M').mean()

select = Select(title="Neighborhood:", value='Mission', options=list(reviews.columns))
source = ColumnDataSource(data=dict(x=[], y=[]))

p = Figure(x_axis_type="datetime", plot_height=600, plot_width=800, title="AirBnB Reviews", toolbar_location=None, tools=TOOLS)
line = p.line(x="x", y="y", source=source)

def update(attrname, old, new):
    p.title = select.value
    source.data = dict(
        x=reviews.index,
        y=reviews[select.value],
    )

select.on_change('value', update)

inputs = HBox(VBoxForm(select), width=300)

update(None, None, None) # initial load of the data

curdoc().add_root(HBox(inputs, p, width=1100))