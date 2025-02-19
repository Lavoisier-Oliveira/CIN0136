import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API"])

# Configurações do modelo de IA
default_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",  # Resposta sempre em JSON
}

class GeminiModel(genai.GenerativeModel):
    def __init__(self, 
                model_name = "gemini-2.0-flash", 
                safety_settings = None, 
                generation_config = default_config, 
                tools = None, 
                tool_config = None, 
                system_instruction = open("model_instructions.txt", encoding="utf8").readlines(),
                ):
        
        super().__init__(model_name, safety_settings, generation_config, tools, tool_config, system_instruction)
        
        self.conversation()

    def send_message(self, prompt : str) -> str:
        try:
            response = self.chat.send_message(prompt)
        except Exception as e:
            print(e)
            return "[]"
        
        return response.text or "[]"
    
    def conversation(self):
        self.chat = self.start_chat()