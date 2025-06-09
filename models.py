from pydantic_ai.models.groq import GroqModel


llama_model = GroqModel(model_name="llama-3.1-8b-instant")
gemma_model = GroqModel(model_name="gemma2-9b-it")
llama_4_model = GroqModel(model_name="meta-llama/llama-4-scout-17b-16e-instruct")
