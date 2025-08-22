from flask import Flask, jsonify, send_file, send_from_directory
from ..workers.main import add_data_task, process_bookmark
from ..rag.utils import rag_query
from ..db.parser import Data
app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query(request):
    try:
        data = request.json()
        query = data['query']
        query_response = rag_query(query)
        return jsonify({"success":True, "data":query_response})
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})

@app.route("/data", methods=["POST"])
def add_data(request):
    try:
        data = request.json()
        data_ = Data(**data)
        if data_.type != "bookmark":
            add_data_task.delay(data_.model_dump())
        return {"success":True, "message":"Data is being indexed"}
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})
if __name__ == "__main__":
    app.run(debug=True)