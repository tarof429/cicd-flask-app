from prefs import Prefs
import yaml

def test_write_then_load_prefs(app):
    with app.app_context():
        prefs = Prefs('tests/data/test_write_then_load_prefs.yaml')
        prefs.write(data = {
            'this': 'that'
        })
        readPrefs = prefs.load()

        assert readPrefs is not None
        assert readPrefs['this'] == 'that'

def test_write_then_load_prefs2(app):
    with app.app_context():
        prefs = Prefs('tests/data/test_write_then_load_prefs.yaml')
        prefs.write(data = {
            'sysadminemail': 'admin@foo.com',
            'notificationDelay': '10'
        })
        readPrefs = prefs.load()

        assert readPrefs is not None
        assert readPrefs['sysadminemail'] == 'admin@foo.com'
        assert readPrefs['notificationDelay'] == '10'

def test_load_prefs(app):
    with app.app_context():
        prefs = Prefs('tests/data/test_load_prefs.yaml')

        readPrefs = prefs.load()

        assert readPrefs is not None
        assert readPrefs == {}

def test_load_write_load_write_load_prefs(app):
    with app.app_context():
        prefs = Prefs('tests/data/test_load_write_load_write_load_prefs.yaml')

        prefs.load()

        prefs.write(data = {
            'foo': 'bar'
        })
        readPrefs = prefs.load()

        assert readPrefs['foo'] == 'bar'

        prefs.write(data = {
            'foo': 'bing'
        })

        readPrefs = prefs.load()
        assert readPrefs['foo'] == 'bing'
