from FakeCSV.celery import app


@app.task
def form_fake_data(schema_id):
    """
    Form csv file with fake data according to schema column types."""
    #TODO
