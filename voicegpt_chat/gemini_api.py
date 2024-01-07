# from google.cloud import aiplatform as aiplatform

# api_key = "AIzaSyBFs2t5pp0sgOYw7W32pxcX_j6kXEA5bFo"
# project_id = "gemini-01-409621"
# model_id = "gemini-pro-text"

# text = "What is the meaning of life?"

# aiplatform.configure(api_key=api_key)

# pipeline_spec = aiplatform.PipelineSpec(
#     display_name="Gemini Pro Text",
#     model_specs=[aiplatform.ModelSpec(model_id, project_id)],
# )

# model = aiplatform.Model.from_pipeline_spec(pipeline_spec)
# prediction = model.predict(text=text)

# print(prediction.text)


# import pathlib
# import textwrap

# import google.generativeai as genai

# # Used to securely store your API key
# from google.colab import userdata

# from IPython.display import display
# from IPython.display import Markdown


# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


# genai.configure(api_key=GOOGLE_API_KEY)


# model = genai.GenerativeModel('gemini-pro')

# %%time
# response = model.generate_content("What is the meaning of life?")


# to_markdown(response.text)

# response.prompt_feedback
# response.candidates

# %%time
# response = model.generate_content("What is the meaning of life?", stream=True)

# for chunk in response:
#   print(chunk.text)
#   print("_"*80)


# curl -o image.jpg https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcQ_Kevbk21QBRy-PgB4kQpS79brbmmEG7m3VOTShAn4PecDU5H5UxrJxE3Dw1JiaG17V88QIol19-3TM2wCHw


# import PIL.Image

# img = PIL.Image.open('image.jpg')


# model = genai.GenerativeModel('gemini-pro-vision')

# response = model.generate_content(img)

# to_markdown(response.text)


# response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
# response.resolve()
# to_markdown(response.text)


# model = genai.GenerativeModel('gemini-pro')
# chat = model.start_chat(history=[])
# chat

# response = chat.send_message("In one sentence, explain how a computer works to a young child.")
# to_markdown(response.text)

# response = chat.send_message("Okay, how about a more detailed explanation to a high schooler?", stream=True)

# for chunk in response:
#   print(chunk.text)
#   print("_"*80)


# for message in chat.history:
#   display(to_markdown(f'**{message.role}**: {message.parts[0].text}'))

# result = genai.embed_content(
#     model="models/embedding-001",
#     content="What is the meaning of life?",
#     task_type="retrieval_document",
#     title="Embedding of single string")

# # 1 input > 1 vector output
# print(str(result['embedding'])[:50], '... TRIMMED]')


# result = genai.embed_content(
#     model="models/embedding-001",
#     content=[
#       'What is the meaning of life?',
#       'How much wood would a woodchuck chuck?',
#       'How does the brain work?'],
#     task_type="retrieval_document",
#     title="Embedding of list of strings")

# # A list of inputs > A list of vectors output
# for v in result['embedding']:
#   print(str(v)[:50], '... TRIMMED ...')

# result = genai.embed_content(
#     model = 'models/embedding-001',
#     content = response.candidates[0].content)

# # 1 input > 1 vector output
# print(str(result['embedding'])[:50], '... TRIMMED ...')

# import pathlib
# import textwrap
# import google.generativeai as genai

# class GeminiAPI:
#     """
#     Gemini API wrapper for local use in a Python environment.
#     """

#     def __init__(self, api_key, project_id):
#         """
#         Initialize the Gemini API wrapper.

#         Args:
#             api_key: Your Google Cloud API key.
#             project_id: The ID of your Google Cloud project.
#         """

#         self.api_key = api_key
#         self.project_id = project_id

#         # Configure the Gemini API
#         genai.configure(api_key=self.api_key)

#     def generate_content(self, text, stream=False):
#         """
#         Generate text using the specified model.

#         Args:
#             text: The text prompt for the model.
#             stream: True to stream the response, False to return it as a single object.

#         Returns:
#             The generated text response.
#         """

#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(text, stream=stream)
#         return response

#     def embed_content(self, model_id, content, task_type="retrieval_document", title=""):
#         """
#         Embed text using the specified model.

#         Args:
#             model_id: The ID of the model to use for embedding.
#             content: The text or image content to embed.
#             task_type: The type of task for which the embedding is used.
#             title: A title for the embedding.

#         Returns:
#             The embedding result.
#         """

#         result = genai.embed_content(
#             model=model_id,
#             content=content,
#             task_type=task_type,
#             title=title
#         )
#         return result

# api_key = "AIzaSyBFs2t5pp0sgOYw7W32pxcX_j6kXEA5bFo"
# project_id = "gemini-01-409621"
# # model_id = "gemini-pro-text"
# api = GeminiAPI(api_key, project_id)

# response = api.generate_content("What is the meaning of life?")
# print(response.text)

# result = api.embed_content("models/embedding-001", "What is the meaning of life?")
# print(result["embedding"])

import logging
import google.generativeai as genai

class GeminiAPI:
    """
    Enhanced Gemini API wrapper for local use in a Python environment.
    """

    def __init__(self, api_key, project_id, default_model='gemini-pro'):
        """
        Initialize the Gemini API wrapper.

        Args:
            api_key (str): Your Google Cloud API key.
            project_id (str): The ID of your Google Cloud project.
            default_model (str): Default model for content generation.
        """

        self.api_key = api_key
        self.project_id = project_id
        self.default_model = default_model

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        logging.basicConfig(level=logging.INFO)
        logging.info("Gemini API configured successfully.")

    def generate_content(self, text, model_id=None, stream=False):
        """
        Generate text using a specified model.

        Args:
            text (str): The text prompt for the model.
            model_id (str): Model ID to use. If None, uses default model.
            stream (bool): True to stream the response, False to return it as a single object.

        Returns:
            str: The generated text response.
        """
        model_id = model_id if model_id else self.default_model
        try:
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(text, stream=stream)
            return self.format_response(response)
        except Exception as e:
            logging.error(f"Error in generate_content: {e}")
            return None

    def embed_content(self, content, model_id="models/embedding-001", task_type="retrieval_document", title=""):
        """
        Embed text using the specified model.

        Args:
            content (str or list): The text or image content to embed.
            model_id (str): The ID of the model to use for embedding.
            task_type (str): The type of task for which the embedding is used.
            title (str): A title for the embedding.

        Returns:
            dict: The embedding result.
        """
        try:
            result = genai.embed_content(
                model=model_id,
                content=content,
                task_type=task_type,
                title=title
            )
            return result
        except Exception as e:
            logging.error(f"Error in embed_content: {e}")
            return None

    @staticmethod
    def format_response(response):
        """
        Format the API response for improved readability.

        Args:
            response (object): The response object from the API.

        Returns:
            str: Formatted response text.
        """
        formatted_text = ""

        if hasattr(response, 'text'):
            response_text = response.text
        elif isinstance(response, dict):
            response_text = "\n".join([f"{k}: {v}" for k, v in response.items()])
        else:
            response_text = str(response)

        # Remove Markdown bullets and bold formatting
        for line in response_text.split("\n"):
            line = line.replace("* ", "")  # Remove bullet points
            line = line.replace("**", "")  # Remove bold formatting
            formatted_text += line + "\n"

        return formatted_text.strip()

    def get_response(self, prompt):
        response = self.generate_content(prompt)
        return self.format_response(response)


# # # Example Usage
# api_key = "AIzaSyBFs2t5pp0sgOYw7W32pxcX_j6kXEA5bFo"
# project_id = "gemini-01-409621"
# api = GeminiAPI(api_key, project_id)

# response = api.generate_content("Actúa como un filósofo cristiano y dime cuáles son los mejores argumentos contra el ateismo")
# print(response)

# embedding_result = api.embed_content("What is the meaning of life?")
# print(embedding_result)
