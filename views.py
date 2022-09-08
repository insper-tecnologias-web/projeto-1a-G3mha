from utils import build_response, delete_note, load_data, load_template, add_note, delete_note, update_note
import urllib.parse as urlparse
from database import Note


def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
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
            print(chave)
        note = Note(title=params['titulo'], content=params['detalhes']) # Cria uma nova nota para o dicionario de parametros
        add_note(note) # Adiciona a nota no banco de dados
        return build_response(code=303, reason='See Other', headers='Location: /')
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template, notes_li = load_template('components/note.html'), []
    for dados in load_data():
        try:
            note = note_template.format(title=dados['titulo'], details=dados['detalhes'])
            notes_li.append(note)
        except:
            print('error')
            continue
    notes = '\n'.join(notes_li)
    body = load_template('index.html').format(notes=notes)
    return build_response() + body.encode()