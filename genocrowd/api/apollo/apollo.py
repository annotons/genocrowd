import time

from apollo import ApolloInstance
# from flask import current_app as ca

from flask import Blueprint, request, session
from flask import current_app as ca

from genocrowd.libgenocrowd.Data import Data
from genocrowd.libgenocrowd.Utils import Utils

import gridfs

apollo_bp = Blueprint('apollo', __name__, url_prefix='/')


@apollo_bp.route('/api/apollo/genechoice', methods=["GET"])
def annotation_start():
    DataInstance = Data(ca, session)
    all_positions = DataInstance.get_all_positions()
    selected_item = Utils.get_random_items(1, all_positions)[0]
    print(selected_item)
    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")
    gff_file = fs.get(selected_item["_id"])
    f = open("./gff.txt", mode="w")
    f.write(gff_file.read().decode('UTF-8'))
    f.close()
    f = open("./gff.txt", mode="r")
    apollo = ApolloInstance("http://localhost:8080/apollo", "admin@admin.fr", "admin")
    apollo.annotations.load_gff3("puceron_%s" % (session["user"]["email"]), f)
    time.sleep(1)
    url = "http://localhost:8080/apollo/annotator/loadLink?loc=%s:%s..%s&organism=puceron_%s" % (selected_item["chromosome"], selected_item["start"], selected_item["end"], session["user"]["email"])
    return url


@apollo_bp.route('api/apollo/save', methods=["POST"])
def annotation_end():
    db = ca.mongo.db
    data = request.files['file']
    fs = gridfs.GridFS(db, collection="answers")
    fs.put(data.read().encode())
    print("i'm saving everything!")
    apollo = ApolloInstance("http://localhost:8080/apollo", "admin@admin.fr", "admin")
    feature_id = apollo.annotations.get_features("puceron_%s" % (session["user"]["email"]))["features"][0]
    gff_file = apollo.annotations.get_gff3(feature_id, "puceron_%s" % (session["user"]["email"]))
    DataInstance = Data(ca, session)
    DataInstance.store_answers_from_user(session["user"]["username"], gff_file)
