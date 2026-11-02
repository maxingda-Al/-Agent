import os
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI
from utils.config_handler import rag_conf
from utils.path_tool import get_abs_path

load_dotenv(get_abs_path(".env"))


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"缺少环境变量 {name}，请复制 .env.example 为 .env 并填写")
    return value


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->Optional[Embeddings | ChatOpenAI]:
        pass
class ChatModelFactory(BaseModelFactory):
    def generator(self) ->Optional[Embeddings | ChatOpenAI]:
        return ChatOpenAI(model=rag_conf["chat_model_name"],
                          api_key=require_env("DEEPSEEK_API_KEY"),
                          base_url=rag_conf["DEEPSEEK_BASE_URL"]
                          )
class EmbeddingsFactory(BaseModelFactory):
    def generator(self) ->Optional[Embeddings | ChatOpenAI]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"],
                                   dashscope_api_key=require_env("DASHSCOPE_API_KEY"),
        )
chat_model=ChatModelFactory().generator()
embed_model=EmbeddingsFactory().generator()
