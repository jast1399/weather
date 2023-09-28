import pytest
from weather.db import get_db

def test_get_forecast(runner,app):
    with app.app_context():
        runner.invoke(args=['get-forecast'])
        db = get_db()
        entries = db.execute('SELECT * FROM forecast').fetchall()
        assert len(entries) > 3

def test_get_history(runner,app):
    with app.app_context():
        runner.invoke(args=['get-history'])
        db = get_db()
        entries = db.execute('SELECT * FROM history').fetchall()
        assert len(entries) > 3