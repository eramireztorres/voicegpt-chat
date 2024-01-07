import os
import openai

class OpenAITTS:
    def __init__(self, api_key=None, model="tts-1", default_voice="alloy", output_format="mp3"):
        self.client = openai.OpenAI(api_key=api_key if api_key else os.environ.get('OPENAI_API_KEY'))
        self.model = model
        self.default_voice = default_voice
        self.output_format = output_format

    def generate_audio(self, text, voice=None, output_path="output.mp3"):
        if voice is None:
            voice = self.default_voice

        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=voice,
                input=text,
                response_format=self.output_format
            )

            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Audio generated and saved to {output_path}")

        except AttributeError as e:
            print(f"An error occurred: {e}")
            print("Please check the latest OpenAI SDK documentation for the correct method to generate audio.")

    def convert_text_to_audio(self, text, output_filename, voice="alloy"):
        # The rate and volume parameters are not used in OpenAITTS, but are included for compatibility
        # subtitle_filename is also not used as OpenAITTS doesn't produce subtitles
        self.generate_audio(text, voice, output_path=output_filename)

# Example usage
# tts = OpenAITTS(api_key="your_openai_api_key")
# tts.convert_text_to_audio("Hello world", "hello_world.mp3", voice="echo")


# Example Usage
#tts = OpenAITTS(api_key="api_key")
# tts.generate_audio("Today is a wonderful day to build something people love!", voice="echo", output_path="today.mp3")

#tts.generate_audio("Esta es una prueba en español, a ver cómo se escucha.", voice="echo", output_path="spanish_today.mp3")
