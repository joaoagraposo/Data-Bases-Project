import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) n_entities FROM ENTIDADE)
    JOIN
      (SELECT COUNT(*) n_contratos FROM CONTRATO)
    JOIN
      (SELECT COUNT(*) n_produtos FROM PRODUTO)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)


@APP.route('/entidade/<int:id>/')
def get_entidade(id):
  entidade = db.execute(
      '''
      SELECT NIF, NOME
      FROM ENTIDADE 
      WHERE NIF = ?
      ''', [id]).fetchone()

  if entidade is None:
     abort(404, 'NIF {} does not exist on this database.'.format(id))

  
  return render_template('entidade.html', 
           entidade=entidade)


@APP.route('/entidade/search/<expr>/')
def search_entidade(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  entidade = db.execute(
      ''' 
      SELECT NIF, NOME
      FROM ENTIDADE 
      WHERE NOME LIKE ?
      ''', [expr]).fetchall()
  return render_template('entity-search.html',
           search=search,entidade=entidade)

@APP.route('/entidade/')
def list_entities():
    entidade = db.execute('''
      SELECT NIF, NOME 
      FROM ENTIDADE
      ORDER BY NOME
    ''').fetchall()
    return render_template('entity-list.html', entidade=entidade)


@APP.route('/contrato/<int:id>/')
def get_contrato(id):

    query = '''
        SELECT c.ID_CONTRATO, c.DESCRICAO, c.DATA, c.VALOR, c.TIPO,
               e.NIF_ENTIDADE, e.TIPO AS TIPO_ENTIDADE, ent.NOME AS NOME_ENTIDADE
        FROM CONTRATO c
        LEFT JOIN CONTRATO_ENTIDADE e ON c.ID_CONTRATO = e.ID_CONTRATO
        LEFT JOIN ENTIDADE ent ON e.NIF_ENTIDADE = ent.NIF
        WHERE c.ID_CONTRATO = ?
    '''

    contrato_info = db.execute(query, [id]).fetchall()

    if not contrato_info:
        abort(404, 'Contract ID {} does not exist.'.format(id))

    contrato = {
        'ID_CONTRATO': contrato_info[0]['ID_CONTRATO'],
        'DESCRICAO': contrato_info[0]['DESCRICAO'],
        'DATA': contrato_info[0]['DATA'],
        'VALOR': contrato_info[0]['VALOR'],
        'TIPO': contrato_info[0]['TIPO'],
        'ENTIDADES': []
    }

    for row in contrato_info:
        if row['NIF_ENTIDADE']:
            entidade = {
                'NIF_ENTIDADE': row['NIF_ENTIDADE'],
                'TIPO_ENTIDADE': row['TIPO_ENTIDADE'],
                'NOME_ENTIDADE': row['NOME_ENTIDADE']
            }
            contrato['ENTIDADES'].append(entidade)

    return render_template('contrato.html', contrato=contrato)


@APP.route('/contrato/search/<expr>/')
def search_contrato(expr):
    search = {'expr': expr}
    expr = '%' + expr + '%'
    contrato = db.execute(
        ''' 
        SELECT ID_CONTRATO, DESCRICAO, DATA, VALOR, TIPO
        FROM CONTRATO 
        WHERE DESCRICAO LIKE ?
        ''', [expr]).fetchall()
    return render_template('contract-searchdes.html', search=search, contrato=contrato)

@APP.route('/contrato/')
def list_contracts():
    contrato = db.execute('''
      SELECT ID_CONTRATO, DESCRICAO, DATA, VALOR, TIPO
      FROM CONTRATO 
      ORDER BY ID_CONTRATO
    ''').fetchall()
    return render_template('contract-list.html', contrato=contrato)

@APP.route('/produto/')
def list_products():
    produto = db.execute('''
      SELECT CPV, NOME
      FROM PRODUTO 
      ORDER BY NOME
    ''').fetchall()
    return render_template('product-list.html', produto=produto)

@APP.route('/produto/<id>/')
def get_produto(id):
  produto = db.execute(
      '''
      SELECT CPV, NOME
      FROM PRODUTO 
      WHERE CPV LIKE ?
      ''', [id]).fetchone()

  if produto is None:
     abort(404, 'CPV {} does not exist on this database.'.format(id))

  
  return render_template('produto.html', 
           produto=produto)

@APP.route('/produto/search/<expr>/')
def search_product(expr):
    search = {'expr': expr}
    expr = '%' + expr + '%'
    produto = db.execute(
        ''' 
      SELECT CPV, NOME
      FROM PRODUTO 
      WHERE NOME LIKE ?
        ''', [expr]).fetchall()
    return render_template('product-search.html', search=search, produto=produto)