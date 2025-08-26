from flask import Flask, jsonify, send_file, send_from_directory, request
from ..workers.main import add_data_task, process_bookmark
from ..rag.utils import rag_query
from ..db.parser import Data, DATA_TYPES
app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json(force=True)
        query = data['query']
        query_response = rag_query(query)
        return jsonify({"success":True, "data":query_response})
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})

@app.route("/data", methods=["POST"])
def add_data():
    try:
        data = request.get_json(force=True)
        data_ = Data(**data)
        if data_.type not in DATA_TYPES:
            raise Exception(f"Data type '{data_.type}' not supported")
        add_data_task.delay(data_.model_dump())
        return {"success":True, "message":"Data is being indexed"}
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})
if __name__ == "__main__":
    app.run(debug=True)