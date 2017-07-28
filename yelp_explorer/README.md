# [Yelp Explorer](https://swetharevanur.github.io/2017/07/28/yelp-explorer.html)

Interactive query tool for Yelp data. Built using Bokeh version 0.12.6 and the Yelp Fusion API. 

I introduced a credibility metric that integrates a business's rating and review count. This ensures that 5-star establishments with 1000 reviews are given a higher score than 5-star establishments with 20 reviews.

To run:
1. Clone and download repository.
2. Update `queryYelp.py` to include your OAuth credentials.
3. Start Bokeh server: `bokeh serve --show main.py`

The application should open in your browser as `http://localhost:5006/main`.

Inspired by the [Bokeh IMDb demo](https://demo.bokehplots.com/apps/movies).

Last updated 07/28/2017.
