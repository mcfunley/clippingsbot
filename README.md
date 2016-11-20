# hello-flask

This is a demo Python ([Flask](http://flask.pocoo.org/)) app you can deploy to [Skyliner](https://www.skyliner.io). Here's a guide to getting started:

[https://www.skyliner.io/help/quick-start](https://www.skyliner.io/help/quick-start)

If you have any trouble, please drop us a line at [support@skyliner.io](mailto:support@skyliner.io?Subject=Help%20with%20hello-flask).

## Differences from a stock Flask application

* In order to work with Application Load Balancers, the `PYTHONUNBUFFERED`
  environment variable needs to be set to `1`.
