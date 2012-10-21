from molly.rest import flask_app

flask_app.debug = True
flask_app.run(debug=True, port=8000)
