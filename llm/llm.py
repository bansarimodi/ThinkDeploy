import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()

# Initialize LLaMA 3 from Groq
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)
