from config import *
from listar import *
from incluir import *
from _init_ import *

with app.app_context():
    db.create_all()
    CORS(app)
    app.run(debug=True, host="0.0.0.0")