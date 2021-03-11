import time
from io import StringIO

from apollo import ApolloInstance
# from flask import current_app as ca

from flask import Blueprint, session
from flask import current_app as ca

from genocrowd.libgenocrowd.Data import Data
from genocrowd.libgenocrowd.Utils import Utils

import gridfs

apollo_bp = Blueprint('apollo', __name__, url_prefix='/')


@apollo_bp.route('/api/apollo/genechoice', methods=["GET"])
def annotation_start():
    """Selects a gene in MongoDB and imports it in the Annotation track

    Returns
    -------
    json
        url: url for the apollo window, centered on the gene position
        attributes: chromosome on which the gene is
    """
    DataInstance = Data(ca, session)
    all_positions = DataInstance.get_all_positions()
    # FIXME error if no gene in db
    selected_item = Utils.get_random_items(1, all_positions)[0]
    ca.logger.info("Selected gene: {}".format(selected_item))

    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")  # FIXME not sure we really need gridfs (small chunks of gff)
    gff_file = fs.get(selected_item["_id"])

    gff_str = StringIO()
    gff_str.write(gff_file.read().decode())

    gff_str.seek(0)

    ca.logger.info("Loading gff: {}".format(gff_str.read()))

    gff_str.seek(0)

    apollo = ApolloInstance(ca.apollo_url, ca.apollo_admin_email, ca.apollo_admin_password)
    apollo.annotations.load_gff3("%s_%s" % (ca.apollo_org_id, session["user"]["email"]), gff_str)

    time.sleep(1)

    url = "%s/annotator/loadLink?loc=%s:%s..%s&organism=%s_%s" % (ca.apollo_url_ext, selected_item["chromosome"], selected_item["start"], selected_item["end"], ca.apollo_org_id, session["user"]["email"])
    DataInstance.update_current_annotation(session["user"]["username"], selected_item)
    return {'url': url}


@apollo_bp.route('api/apollo/save', methods=["POST"])
def annotation_end():
    """gets the new annotation and saves it in mongodb"""
    DataInstance = Data(ca, session)
    current_gene = DataInstance.get_current_annotation(session["user"]["username"])
    apollo = ApolloInstance(ca.apollo_url, ca.apollo_admin_email, ca.apollo_admin_password)
    features = apollo.annotations.get_features(organism="%s_%s" % (ca.apollo_org_id, session["user"]["email"]), sequence=current_gene["chromosome"])["features"]
    gff_file = apollo.annotations.get_gff3(features[0]["uniquename"], "%s_%s" % (ca.apollo_org_id, session["user"]["email"]))
    DataInstance.store_answers_from_user(session["user"]["username"], gff_file)
    apollo.organisms.delete_features("%s_%s" % (ca.apollo_org_id, session["user"]["email"]))
    return {'error': False, 'errorMessage': 'no error'}
