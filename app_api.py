from flask import Flask, request, jsonify, redirect
from models import URL, User, Session, create_tables
from datetime import datetime, timedelta
from flask_jwt_extended import ( JWTManager, create_access_token, jwt_required, get_jwt_identity )
from flasgger import Swagger
import random
import string

app = Flask(__name__)
create_tables()

swagger = Swagger(app)

app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_super_segura'
jwt = JWTManager(app)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Encurtador de URL com Flask",
        "description": "API com autenticação JWT, expiração e limite de acessos",
        "version": "1.0"
    },
    "basePath": "/",
})

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Informe usuário e senha'}), 400

    session = Session()
    if session.query(User).filter_by(username=username).first():
        session.close()
        return jsonify({'error': 'Usuário já existe'}), 409

    user = User(username=username)
    user.set_password(password)
    session.add(user)
    session.commit()
    session.close()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if not user or not user.check_password(password):
        session.close()
        return jsonify({'error': 'Credenciais inválidas'}), 401

    access_token = create_access_token(identity=user.id)
    session.close()
    return jsonify({'access_token': access_token})

@app.route('/admin/urls', methods=['GET'])
@jwt_required()
def list_user_urls():
    """
    Lista URLs criadas pelo usuário autenticado
    ---
    tags:
      - Admin
    responses:
      200:
        description: Lista de URLs
    """
    user_id = get_jwt_identity()
    session = Session()
    urls = session.query(URL).filter_by(user_id=user_id).all()
    session.close()

    result = []
    for url in urls:
        result.append({
            "original_url": url.original_url,
            "short_url": request.host_url + url.short_code,
            "created_at": url.created_at,
            "expires_at": url.expires_at,
            "max_visits": url.max_visits,
            "visit_count": url.visit_count
        })

    return jsonify(result)

@app.route('/shorten', methods=['POST'])
@jwt_required()
def shorten_url():
    """
    Encurta uma URL
    ---
    tags:
      - URLs
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            url:
              type: string
            expires_in_days:
              type: integer
            max_visits:
              type: integer
    responses:
      200:
        description: URL encurtada com sucesso
      400:
        description: Erro de validação
      401:
        description: Token ausente ou inválido
    """
    
    current_user_id = get_jwt_identity()
    data = request.get_json()
    original_url = data.get('url')
    custom_code = data.get('custom_code')
    expires_in_days = data.get('expires_in_days')
    max_visits = data.get('max_visits')

    if not original_url:
        return jsonify({'error': 'URL não fornecida'}), 400

    session = Session()

    # Define a data de expiração, se houver
    expires_at = None
    if expires_in_days:
        try:
            expires_at = datetime.utcnow() + timedelta(days=int(expires_in_days))
        except:
            session.close()
            return jsonify({'error': 'expires_in_days inválido'}), 400

    # Verifica se o custom_code já está em uso
    if custom_code:
        if session.query(URL).filter_by(short_code=custom_code).first():
            session.close()
            return jsonify({'error': 'Este código já está em uso. Escolha outro.'}), 409
        short_code = custom_code
    else:
        # Geração de código aleatório único
        while True:
            short_code = generate_short_code()
            if not session.query(URL).filter_by(short_code=short_code).first():
                break

    # Criação e salvamento
    new_url = URL(
        original_url=original_url,
        short_code=short_code,
        user_id=current_user_id,
        expires_at=expires_at,
        max_visits=max_visits
    )

    session.add(new_url)
    session.commit()
    session.close()

    return jsonify({'short_url': request.host_url + short_code}), 200

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    session = Session()
    url = session.query(URL).filter_by(short_code=short_code).first()

    if not url:
        session.close()
        return jsonify({'error': 'URL não encontrada'}), 404

    if url.expires_at and datetime.utcnow() > url.expires_at:
        session.close()
        return jsonify({'error': 'URL expirada'}), 410

    if url.max_visits is not None and url.visit_count >= url.max_visits:
        session.close()
        return jsonify({'error': 'Limite de acessos excedido'}), 429

    url.visit_count += 1
    session.commit()
    session.close()

    return redirect(url.original_url)

if __name__ == '__main__':
    app.run(debug=True)
