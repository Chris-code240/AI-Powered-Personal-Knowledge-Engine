from app.db.parser import Data
from app.workers.main import add_data_task
from app.db.connection import session_connection

data = Data(metadata_={"title":"Computer Graphicts"}, type="pdf", data_path="app/workers/Computer graphics - Wikipedia.pdf")

add_data_task.delay(data.model_dump())

