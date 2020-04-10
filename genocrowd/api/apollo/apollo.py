# from flask import current_app as ca
from flask import Blueprint, session, request
from flask import current_app as ca

from apollo import ApolloInstance
from genocrowd.api.auth.login import login_required
from genocrowd.libgenocrowd.Apollo import Data
from genocrowd.libgenocrowd.Utils import Utils

apollo_bp = Blueprint('apollo', __name__, url_prefix='/')


@apollo_bp.route('/api/apollo/genechoice', methods=["GET"])
def annotation_start():
    DataInstance = Data(ca, session)
    all_positions = DataInstance.get_all_positions()
    selected_item = Utils.get_random_items(1, all_positions)
    # go to position
    # display position
    return selected_item
