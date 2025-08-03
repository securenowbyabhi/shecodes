from flask import Blueprint, request
from ..controllers.auth_controller import handle_register, handle_login , handle_project_status

# Author : av42956 
# InIT_FILE : All APIs will be declared here
 
auth_bp = Blueprint('shecodes', __name__, url_prefix='/shecodes')

@auth_bp.route('/signup', methods=['POST'])
def register():
    return handle_register(request)



@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Flask-CORS usually handles this, but you can also explicitly return empty response
            return '', 200
    return handle_login(request)



@auth_bp.route('/projectstatus', methods=['GET'])  
def project_status():
    return handle_project_status(request)
