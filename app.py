import os
from flask import Flask
from extensions import db, login_manager, csrf

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    from routes.videos import videos_bp
    from routes.simulados import simulados_bp
    from routes.materiais import materiais_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(videos_bp, url_prefix='/videoaulas')
    app.register_blueprint(simulados_bp, url_prefix='/simulados')
    app.register_blueprint(materiais_bp, url_prefix='/materiais')
    
    with app.app_context():
        db.create_all()
        create_admin_user()
    
    return app

def create_admin_user():
    from models import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(email='admin@nerdsplantao.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@nerdsplantao.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            is_approved=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created: admin@nerdsplantao.com / admin123')

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
