# -----------------------
# CONFIGURATION
# -----------------------
MODEL_PATH = "app/rag/phi-3-mini-4k-instruct-q4.gguf"
COLLECTION_NAME = "data_chunks"

n_ctx = 4096
n_threads = 6  # Adjust based on CPU cores
n_batch = 512
