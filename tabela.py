from config import *
from Jogada import *

# apagar o arquivo, se houver
if os.path.exists(arquivobd):
    os.remove(arquivobd)
    
with app.app_context():    
    db.create_all()

print("Tabelas criadas")
