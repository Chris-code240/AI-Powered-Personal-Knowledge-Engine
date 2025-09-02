from flask import Flask, jsonify, request
from ..workers.main import add_data_task
from ..rag.utils import rag_query
from ..db.parser import Data, DATA_TYPES
from ..db.models import Data as Data_in_DB, Tag as Tag_in_DB, Chunk
from ..db.connection import session_connection
from sqlalchemy import func, case
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    


@app.route('/report')
def get_report():
    try:

        ingestion_over_time = {}
        data = {}
        with session_connection() as session:
            ingestion_over_time = (
                session.query(
                    func.date(Data_in_DB.created_at).label("date"),
                    func.count(Data_in_DB.id).label("count")
                )
                .group_by(func.date(Data_in_DB.created_at))
                .order_by(func.date(Data_in_DB.created_at))
                .all())
            data['ingestionOverTime'] = [{"date": str(r.date), "count": r.count} for r in ingestion_over_time]
            data_tag_ingestion = [{"tag": tag, "count": count} for tag, count  in   (
                    session.query(
                        Tag_in_DB.label.label("tag"),
                        func.count(Tag_in_DB.id).label("count")
                    )
                    .group_by(Tag_in_DB.label)
                    .all()
            )]
            data['tagDistribution'] = data_tag_ingestion

            results_top_sources = (
    session.query(
        case(
            (
                Data_in_DB.data_path.like('http%'),
                func.substr(
                    Data_in_DB.data_path,
                    func.strpos(Data_in_DB.data_path, '//') + 2
                )
            ),
            else_='local'
        ).label('source'),
        func.count(Data_in_DB.id).label('count')
    )
    .group_by('source')
    .all()
)

            data_top_sources = []
            for source, count in results_top_sources:
                if source != 'local':
                    source = source.split('/')[0]  # keep domain only
                data_top_sources.append({"source": source, "count": count})
            data['topSources'] = data_top_sources

            results_embedding_coverage = (
                session.query(
                    Data_in_DB.has_been_indexed.label("status"),
                    func.count(Data_in_DB.id).label("count")
                )
                .group_by(Data_in_DB.has_been_indexed)
                .all()
            )

            data_embedding_coverage = [
                {
                    "status": "Success" if status else "Failed",
                    "percentage": round((count / len(ingestion_over_time)) * 100, 2)
                }
                for status, count in results_embedding_coverage
            ]

            data['embeddingCoverage'] = data_embedding_coverage
        return jsonify({"success":True, "data":data}), 200

    except Exception as e:
        return jsonify({"success":False, "details":str(e)}), 400
    

if __name__ == "__main__":
    app.run(debug=True)