from utils import build_response, delete_note, load_data, load_template, add_note, delete_note, update_note
import urllib.parse as urlparse
from database import Note


def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            valor = urlparse.unquote_plus(valor, encoding='utf-8')
            params[chave] = valor
        note = Note(title=params['titulo'], content=params['detalhes']); add_note(note)
        return build_response(code=303, reason='See Other', headers='Location: /')
    note_template, notes_lista = load_template('components/note.html'), []
    for dados in load_data():
        try:
            note = note_template.format(title=dados['titulo'], details=dados['detalhes'])
            notes_lista.append(note)
        except:
            print('error')
            continue
    notes = '\n'.join(notes_lista)
    body = load_template('index.html').format(notes=notes)
    return build_response() + body.encode()