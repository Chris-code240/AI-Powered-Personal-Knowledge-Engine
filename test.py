from app.db.parser import Data, is_url
from app.workers.main import add_data_task, process_bookmark, scrape_url
from app.db.connection import session_connection
from app.rag.utils import rag_query

print(rag_query("What is recursion?"))

