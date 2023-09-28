import pytest
import weather.data_analysis as da
from weather.db import get_db


def test_get_forecast(app):
    with app.app_context():
        entries = list(da.get_forecast_data())
        assert len(entries[0]) is 3

def test_get_history(app):
    with app.app_context():
        entries = list(da.get_history_data())
        assert len(entries[0]) is 3

def test_get_diff(app):
    with app.app_context():
        entries = list(da.get_diff())
        assert len(entries[0]) is 2

def test_plot(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_plot():
        Recorder.called = True

    monkeypatch.setattr('weather.data_analysis.generate_plot', fake_plot)
    result = runner.invoke(args=['plot-data'])
    assert 'Plot' in result.output
    assert Recorder.called
