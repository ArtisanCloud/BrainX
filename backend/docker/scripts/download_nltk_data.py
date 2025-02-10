# download_nltk_data.py
import nltk

# 下载 stopwords 和 punkt 数据
nltk.download('stopwords', download_dir='/app/dist/server/_internal/llama_index/core/_static/nltk_cache')
nltk.download('punkt', download_dir='/app/dist/server/_internal/llama_index/core/_static/nltk_cache')
