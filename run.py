#!flask/bin/python


from app import app

app.run(ssl_context='adhoc', threaded=True, debug=False)