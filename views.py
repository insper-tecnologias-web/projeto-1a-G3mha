from utils import load_data, load_template, write_json, build_response
import urllib.parse as urlparse
from database import Database, Note


def index(request):
    db = Database('notes')
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]

        is_delete = corpo.split("=")[0] == 'delete'
        if is_delete:
            id = int(corpo.split("=")[1])
            db.delete(id)
        if not is_delete:
            params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            valor = urlparse.unquote_plus(valor, encoding='utf-8')
            params[chave] = valor
        db.add(Note(None, params['titulo'], params['detalhes']))

    
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = []
    for dados in load_data('notes.json'):
        try:
            note = note_template.format(title=dados['titulo'], details=dados['detalhes'])
            notes_li.append(note)
        except:
            print('erro no loop do load_data do views.py')
            continue
    notes = '\n'.join(notes_li)
    body = load_template('index.html').format(notes=notes)
    return build_response() + body.encode()
