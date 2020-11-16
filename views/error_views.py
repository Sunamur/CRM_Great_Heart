
from flask import  render_template, Blueprint

error_blueprint = Blueprint('error', __name__, template_folder='templates')

@error_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404