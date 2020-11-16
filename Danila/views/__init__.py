from .main_views import main_blueprint
from .partner_views import partner_blueprint
from .client_views import client_blueprint
from .sponsor_views import sponsor_blueprint
from .benefactor_views import benefactor_blueprint

def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(partner_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(benefactor_blueprint)