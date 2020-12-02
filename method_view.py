from flask.views import MethodView
from flask import jsonify, request
from ABC.functions import DataStoreABC


class CreatingData(MetView):
    def __init__(self, db_path):
        self.db_path = db_path

    def POST_MET(self):
        try:
            datajson = request.get_json(force=True)
        except Exception:
            return jsonify({"status": "error", "message": "Incorrect request data format. Only JSON object is acceptable."}), 400

        valid_data, msg = DataStoreABC().creating_data(datajson, self.db_path)
        if not valid_data:
            return jsonify({"status": "error", "message": message}), 400

        return jsonify({"status": "success", "message": message}), 200


class ReadingData(MetView):
    def __init__(self, db_path):
        self.db_path = db_path

    def get(self):
        key = request.args.get('key')
        if key is None:
            return jsonify({"status": "error", "message": "key is required as a query param."}), 400

        data_found, msg = DataStoreABC().reading_data(key, self.db_path)
        if not data_found:
            return jsonify({"status": "error", "message": message}), 404

        return jsonify(msg), 200


class DeletingData(MetView):
    def __init__(self, db_path):
        self.db_path = db_path

    def delete(self):
        key = request.args.get('key')

        if key is None:
            return jsonify({"status": "error", "message": "key is required as a query param."}), 400

        data_found, msg = DataStoreABC().deleting_data(key, self.db_path)
        if not data_found:
            return jsonify({"status": "error", "message": message}), 404

        return jsonify({"status": "success", "message": message}), 200
