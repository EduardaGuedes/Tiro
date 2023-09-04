from config import *
from listar import *

# rota padrão
@app.route("/")
def inicio():
    return 'backend com rotas generalizadas de listagem' + '<br>' + \
    '<a href="http://localhost:5000/listar">Clique aqui para listar</a>'

# inserindo a aplicação em um contexto :-/
with app.app_context():

    app.run(debug=True)