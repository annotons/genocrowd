# from flask import current_app as ca
from flask import Blueprint

from genocrowd.api.auth.login import login_required


apollo_bp = Blueprint('apollo', __name__, url_prefix='/')


@apollo_bp.route('/api/auth/questionloader', methods=["GET"])
@login_required
def question_loader():
    print("work in progress")
