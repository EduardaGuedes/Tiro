from config import *
from Jogada import *

@app.route("/incluir/<string:classe>", methods=["post"])
def incluir(classe):
    dados = request.get_json()

    try:
        nova = None
        if classe == "Jogada":
            nova = Jogada(**dados)

        db.session.add(nova)
        db.session.commit()
        resposta = jsonify({"resultado": "Score adicionado!"})

    except Exception as error:
        resposta = jsonify({"resultado": "Erro!", "detalhes": str(error)})

    return resposta