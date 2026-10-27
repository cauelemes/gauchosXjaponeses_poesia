"""
    Módulo compartilhado para invocar cliente da Together AI
"""
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together()  



