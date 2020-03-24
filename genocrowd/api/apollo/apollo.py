# from flask import current_app as ca
from flask import Blueprint, session
from flask import current_app as ca

from genocrowd.api.auth.login import login_required
from genocrowd.libgenocrowd.Apollo import Data
from genocrowd.libgenocrowd.Utils import Utils

apollo_bp = Blueprint('apollo', __name__, url_prefix='/')


@apollo_bp.route('/api/apollo/genechoice', methods=["GET"])
def annotation_start():
    DataInstance = Data(ca, session)
    all_positions = DataInstance.get_all_positions()
    selected_item = Utils.get_random_items(1, all_positions)
    return selected_item


@apollo_bp.route('/api/apollo/questionloader', methods=["GET"])
@login_required
def question_loader():
    print("work in progress")
