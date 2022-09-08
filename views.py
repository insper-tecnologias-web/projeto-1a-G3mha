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

        if ('create' in params.keys()): # Se o parametro create estiver no dicionario de parametros
            add_note(note) # Adiciona a nota no banco de dados
        
        elif ('update' in params.keys()): # se o botao de update for clicado
            note_anterior = Note(title=params['prev_ttl'],content=params['prev_dtl']) # Cria uma nova nota com os valores anteriores
            update_note(note_anterior, note) # Atualiza a nota no banco de dados
        
        elif ('delete' in params.keys()):
            # Deleta a nota selecionada
            delete_note(note)

        return build_response(code=303, reason='See Other', headers='Location: /')
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template, notes_li = load_template('components/note.html'), []
    for note in load_data():
        notes_li.append(note_template.format(title=note.title, details=note.content))
    notes = '\n'.join(notes_li)
    return build_response(load_template('index.html').format(notes=notes))
