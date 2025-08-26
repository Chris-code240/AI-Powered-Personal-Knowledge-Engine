from llama_cpp import Llama
from ..retriever.hybrid_retriever import HybridRetriever
from .import config
from ..retriever.vector_retriever import VectorRetriever


retriever = VectorRetriever()

llm = Llama(
    model_path=config.MODEL_PATH,
    n_ctx=config.n_ctx,
    n_threads=config.n_threads,
    n_batch=config.n_batch
)


