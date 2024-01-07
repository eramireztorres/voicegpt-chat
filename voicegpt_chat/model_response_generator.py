from voicegpt_chat.gpt import Gpt4AnswerGenerator
from voicegpt_chat.gemini_api import GeminiAPI
import os

class ResponseGeneratorInterface:
    """
    Interface for response generators.
    """
    def get_response(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")


# class ModelResponseGenerator:
#     def __init__(self, model='gpt-4-turbo', model_kwargs=None):
#         self.model = model
#         self.model_kwargs = model_kwargs if model_kwargs else {}

#         if 'gpt' in self.model.lower():
#             self.api_key = os.getenv('OPENAI_API_KEY')
#             if not self.api_key:
#                 raise ValueError("OPENAI_API_KEY is required for GPT models but not found in environment variables.")
#             self.response_generator = Gpt4AnswerGenerator(self.api_key, model=self.model)
#         elif 'gemini' in self.model.lower():
#             self.api_key = os.getenv('GEMINI_API_KEY')
#             if not self.api_key:
#                 raise ValueError("GEMINI_API_KEY is required for Gemini models but not found in environment variables.")
#             self.response_generator = GeminiAPI(self.api_key, **self.model_kwargs)
#         else:
#             raise ValueError("Unsupported model type")

#     def get_response(self, prompt):
#         return self.response_generator.get_response(prompt)

class ModelResponseGenerator:
    def __init__(self, model='gpt-3.5-turbo', model_kwargs=None):
        self.model = model
        self.model_kwargs = model_kwargs if model_kwargs else {}

        if 'gpt' in self.model.lower():
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY is required for GPT models but not found in environment variables.")
            self.response_generator = Gpt4AnswerGenerator(self.api_key, model=self.model)
        elif 'gemini' in self.model.lower():
            self.api_key = os.getenv('GEMINI_API_KEY')
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY is required for Gemini models but not found in environment variables.")
            
            project_id = self.model_kwargs.pop('project_id', None)  # Extract project_id from kwargs
            self.response_generator = GeminiAPI(self.api_key, project_id=project_id, **self.model_kwargs)
        else:
            raise ValueError("Unsupported model type")

    def get_response(self, prompt):
        return self.response_generator.get_response(prompt)


# Example usage
# Ensure that the appropriate environment variable (OPENAI_API_KEY or GEMINI_API_KEY) is set
# generator = ModelResponseGenerator(model='gpt-4', model_kwargs={"max_tokens": 1024})
# generator = ModelResponseGenerator(model='gemini-pro', model_kwargs={'project_id' : "gemini-01-409621"})
# response = generator.get_response("La siguiente es una lista de teorías para explicar el comportamiento humano:")
# print(response)
