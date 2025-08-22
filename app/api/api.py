from flask import Flask, jsonify, send_file, send_from_directory
from ..workers.main import add_data_task, process_bookmark
from ..db.parser import Data
app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query(request):
    try:
        return jsonify({"success":True, "data":[]})
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})

@app.route("/data", methods=["POST"])
def add_data(request):
    try:
        """
        1. check data type
        2. create Data instance
        3. if Data(...).type != "bookmark"
        4. pass Data(...).model_dump() to add_data_task()
        5. else
        6. pass Data(...).model_dump() to process_bookmark()
        """
        return {"success":True, "message":"Data is being indexed"}
    except Exception as e:
        return jsonify({"success":False, "message":str(e)})
if __name__ == "__main__":
    app.run(debug=True)