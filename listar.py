from config import *
from Jogada import *

@app.route("/listar")
def listar():
    # obter dados da classe
    dados = db.session.query(Jogada).all()
    if dados:
      # converter dados para json
      lista_jsons = [x.json() for x in dados]

      meujson = {"resultado": "ok"}
      meujson.update({"detalhes": lista_jsons})
      return jsonify(meujson)
    else:
      return jsonify({"resultado":"erro", "detalhes":"classe informada inválida: "})