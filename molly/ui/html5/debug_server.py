import os.path

from molly.ui.html5.server import flask_app

flask_app.debug = True
flask_app.static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
flask_app.static_url_path='static'
print flask_app.static_folder
flask_app.run(debug=True, port=8002)
