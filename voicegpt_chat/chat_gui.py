import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar
from tkinter import ttk
import threading
import speech_recognition as sr
import datetime
import os
import pygame
# from model_response_generator import ModelResponseGenerator
# from edge_tts import EdgeTTS
# from gpt_tts import OpenAITTS
from voicegpt_chat.model_response_generator import ModelResponseGenerator
from voicegpt_chat.edge_tts import EdgeTTS
from voicegpt_chat.gpt_tts import OpenAITTS
import tkinter.simpledialog as simpledialog


import tempfile

# Helper function to get the path of a file in the config directory
def get_config_path(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'config', filename)

import pkg_resources

def read_config_file(filename):
    resource_path = pkg_resources.resource_filename('voicegpt_chat', f'config/{filename}')
    with open(resource_path, 'r') as file:
        return file.read().splitlines()


# Now use read_config_file instead of read_file_from_package
def read_models_from_file():
    return read_config_file('models.txt')

def read_voices_from_file():
    return read_config_file('voices.txt')

def read_kwargs_from_file(file_path):
    kwargs = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                kwargs[key] = value
    except:
        print("Using default model kwargs")
    return kwargs

def read_speech_languages():
    resource_path = pkg_resources.resource_filename('voicegpt_chat', 'config/speech_language.txt')
    with open(resource_path, 'r') as file:
        return file.read().splitlines()


class SpeechToText:
    def __init__(self, language='es-US'):
        self.language = language
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Say something!")
            # audio = self.recognizer.listen(so urce)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ChatGPT Voice Chat")

        
        # Load voices and models from files using the new functions
        self.voices = read_voices_from_file()
        self.models = read_models_from_file()
        self.speech_languages = read_speech_languages()
        
        # Initialize speech_language_selector with default value
        self.speech_language_selector = tk.StringVar(value=self.speech_languages[0] if self.speech_languages else 'es-US')
       

        # API Key Information Label
        self.api_key_label = tk.Label(self.root, text="OPENAI_API_KEY environment variable required\n(optional GEMINI_API_KEY: also requires project-id  in options) ")
        self.api_key_label.pack(pady=(5, 10))

        # Frame for Comboboxes
        self.combobox_frame = tk.Frame(self.root)
        self.combobox_frame.pack(pady=10)

        # Voice Selector
        self.voice_selector_label = tk.Label(self.combobox_frame, text="Select Voice:")
        self.voice_selector_label.grid(row=0, column=0, padx=5)
        self.voice_selector = ttk.Combobox(self.combobox_frame, values=self.voices)
        self.voice_selector.grid(row=0, column=1, padx=5)
        self.voice_selector.bind('<<ComboboxSelected>>', self.change_focus)

        # Model Selector
        self.model_selector_label = tk.Label(self.combobox_frame, text="Select Model:")
        self.model_selector_label.grid(row=1, column=0, padx=5)
        self.model_selector = ttk.Combobox(self.combobox_frame, values=self.models)
        self.model_selector.grid(row=1, column=1, padx=5)
        self.model_selector.bind('<<ComboboxSelected>>', self.change_focus)

        # Text Editor and Response
        self.create_text_editor()

        # Speech and Control Buttons
        self.create_buttons()

        # Initialize other components
        # self.speech_to_text = SpeechToText()
        self.create_menu()
        self.temp_dir = tempfile.mkdtemp()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set default selections if available
        if self.voices:
            self.voice_selector.set(self.voices[0])
        if self.models:
            self.model_selector.set(self.models[0])
     
        self.current_model = None
        self.model_response_generator = None
        self.initialize_model_response_generator()

        # Initialize speech-to-text with the default language
        default_speech_language = self.read_default_speech_language()
        self.speech_to_text = SpeechToText(language=default_speech_language)        
        
        # # Initialize speech_language_selector with default value
        # self.speech_languages = read_file_from_package('config/speech_language.txt')
        # self.speech_language_selector = tk.StringVar(value=self.speech_languages[0] if self.speech_languages else 'es-US')



    def initialize_model_response_generator(self):
        selected_model = self.model_selector.get() or 'gpt-4'
        model_kwargs = self.get_model_kwargs(selected_model)
        self.model_response_generator = ModelResponseGenerator(model=selected_model, model_kwargs=model_kwargs)
        self.current_model = selected_model


    def read_default_speech_language(self):
        # Attempt to read the default speech language from file
        try:
            # Use pkg_resources to locate the file within the package
            file_path = pkg_resources.resource_filename('voicegpt_chat', 'config/speech_language.txt')
            with open(file_path, "r") as file:
                languages = file.read().splitlines()
                if languages:
                    return languages[0]  # Return the first language listed
        except FileNotFoundError:
            print("speech_language.txt not found. Using default language 'es-US'.")
        
        return 'es-US'  # Default language if file is not found or empty
    


    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.options_menu = tk.Menu(self.menu, tearoff=False)
        # self.options_menu.add_command(label="Set API Key", command=self.set_api_key)
        self.options_menu.add_command(label="Set Speech Language", command=self.set_speech_language)

        # Submenu for setting Gemini project ID
        self.gemini_menu = tk.Menu(self.options_menu, tearoff=False)
        self.gemini_menu.add_command(label="Set Gemini project ID", command=self.set_gemini_project_id)
        self.options_menu.add_cascade(label="Gemini Settings", menu=self.gemini_menu)

        self.menu.add_cascade(label="Options", menu=self.options_menu)
        
       # Models Menu
        self.models_menu = tk.Menu(self.options_menu, tearoff=False)
        self.models_menu.add_command(label="Add Model", command=self.add_model)
        self.models_menu.add_command(label="Remove Model", command=self.remove_model)
        self.models_menu.add_command(label="Edit Model", command=self.edit_model)
        self.options_menu.add_cascade(label="Model Settings", menu=self.models_menu)

    def add_model(self):
        # Function to add a new model
        new_model = simpledialog.askstring("Add Model", "Enter model name:")
        if new_model:
            models_file_path = pkg_resources.resource_filename('voicegpt_chat', 'config/models.txt')
            with open(models_file_path, 'a') as file:
                file.write(f"{new_model}\n")
            self.update_models_combobox()

    def remove_model(self):
        # Function to remove an existing model
        model_to_remove = simpledialog.askstring("Remove Model", "Enter model name to remove:")
        if model_to_remove:
            models_file_path = pkg_resources.resource_filename('voicegpt_chat', 'config/models.txt')
            with open(models_file_path, 'r') as file:
                models = file.readlines()
            
            models = [model.strip() for model in models if model.strip() != model_to_remove]
            
            with open(models_file_path, 'w') as file:
                file.writelines([model + '\n' for model in models])
            
            self.update_models_combobox()


    def edit_model(self):
        # Function to edit an existing model
        model_to_edit = simpledialog.askstring("Edit Model", "Enter model name to edit:")
        if model_to_edit:
            new_model_name = simpledialog.askstring("Edit Model", "Enter new model name:")
            if new_model_name:
                models_file_path = pkg_resources.resource_filename('voicegpt_chat', 'config/models.txt')
                with open(models_file_path, 'r') as file:
                    models = file.readlines()
                
                models = [new_model_name + '\n' if model.strip() == model_to_edit else model for model in models]
                
                with open(models_file_path, 'w') as file:
                    file.writelines(models)
                
                self.update_models_combobox()


    def update_models_combobox(self):
        # Update the models list and combobox
        self.models = read_models_from_file()
        self.model_selector['values'] = self.models

        if self.models:
            self.model_selector.set(self.models[0])
        else:
            self.model_selector.set('')


    def set_speech_language(self):
        # Read the available speech languages from file
        self.speech_languages = read_speech_languages()

        # Create a new top-level window
        speech_language_window = tk.Toplevel(self.root)
        speech_language_window.title("Set Speech Language")

        # Combobox for speech language selection
        self.speech_language_selector = ttk.Combobox(speech_language_window, values=self.speech_languages)
        self.speech_language_selector.pack(padx=10, pady=10)
        self.speech_language_selector.bind('<<ComboboxSelected>>', self.change_speech_language)
        if self.speech_languages:
            self.speech_language_selector.set(self.read_current_speech_language())
        
        


    def change_speech_language(self, event=None):
        selected_language = self.speech_language_selector.get()
        self.speech_to_text.language = selected_language
        messagebox.showinfo("Success", f"Speech language changed to {selected_language}.")


    # Function to set the Gemini project ID
    def set_gemini_project_id(self):
        # Read the current project ID from file
        current_project_id = self.read_gemini_project_id()

        # Create a new top-level window
        project_id_window = tk.Toplevel(self.root)
        project_id_window.title("Set Gemini Project ID")

        # Entry for project ID
        project_id_entry = tk.Entry(project_id_window, width=30)
        project_id_entry.pack(padx=10, pady=10)
        project_id_entry.insert(0, current_project_id)  # Prefill with current ID

        # Save button
        save_button = tk.Button(project_id_window, text="Save", command=lambda: self.save_gemini_project_id(project_id_entry.get(), project_id_window))
        save_button.pack(pady=(0, 10))

    def read_gemini_project_id(self):
        try:
            with open("gemini_kwargs.txt", "r") as file:
                for line in file:
                    if line.startswith("project_id"):
                        return line.split('=')[1].strip()
        except FileNotFoundError:
            pass
        return ""

    def save_gemini_project_id(self, project_id, window):
        with open("gemini_kwargs.txt", "w") as file:
            file.write(f"project_id={project_id}\n")
        window.destroy()
        messagebox.showinfo("Success", "Gemini project ID updated successfully.")


    # def set_api_key(self):
    #     messagebox.showinfo("Set API Key", "Please enter your OpenAI API Key.")

    def create_text_editor(self):
        # Text Editor Frame
        self.text_editor_frame = tk.Frame(self.root)
        self.text_editor_frame.pack(pady=10, fill='both', expand=True)
    
        # Create a subframe for the prompt area
        self.prompt_frame = tk.Frame(self.text_editor_frame)
        self.prompt_frame.pack(side=tk.LEFT, fill='both', expand=True)
    
        # Prompt Label and Text
        self.prompt_label = tk.Label(self.prompt_frame, text="Prompt (press Control+P to speak):")
        self.prompt_label.pack(side=tk.TOP, anchor='w')
        self.prompt_text = tk.Text(self.prompt_frame, height=10, width=50, wrap=tk.WORD)
        self.prompt_scroll = Scrollbar(self.prompt_frame, command=self.prompt_text.yview)
        self.prompt_text['yscrollcommand'] = self.prompt_scroll.set
        self.prompt_text.pack(side=tk.LEFT, fill='both', expand=True)
        self.prompt_scroll.pack(side=tk.RIGHT, fill='y')
        self.prompt_text.bind('<Return>', self.on_enter_pressed)
    
        # Create a subframe for the response area
        self.response_frame = tk.Frame(self.text_editor_frame)
        self.response_frame.pack(side=tk.LEFT, fill='both', expand=True)
    
        # Response Label and Text
        self.response_label = tk.Label(self.response_frame, text="Response:")
        self.response_label.pack(side=tk.TOP, anchor='w')
        self.response_text = tk.Text(self.response_frame, height=10, width=50, wrap=tk.WORD)
        self.response_scroll = Scrollbar(self.response_frame, command=self.response_text.yview)
        self.response_text['yscrollcommand'] = self.response_scroll.set
        self.response_text.pack(side=tk.LEFT, fill='both', expand=True)
        self.response_scroll.pack(side=tk.RIGHT, fill='y')

        # Create the Copy Response Button
        self.copy_button = tk.Button(self.response_frame, text="Copy Response", command=self.copy_response_to_clipboard)
        # Initially hide the button
        self.copy_button.pack_forget()


    def copy_response_to_clipboard(self):
        # Function to copy response text to clipboard
        response_text = self.response_text.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(response_text)
        messagebox.showinfo("Copied", "Response text copied to clipboard")


    def on_enter_pressed(self, event=None):
        # Prevents the default newline insertion on pressing Enter
        if event:
            event.widget.master.focus()  # To move focus out of the text widget
            self.submit_prompt()
            return 'break'  # This prevents the default behavior of the Enter key


    def create_buttons(self):
        self.speech_button = tk.Button(self.root, text="Start Speech", command=self.start_speech)
        self.speech_button.pack()

        # Bind key short-cut to the speech button
        self.root.bind('<Control-p>', lambda event: self.start_speech())
        # self.root.bind('<space>', lambda event: self.start_speech())
        
        self.load_button = tk.Button(self.root, text="Load Prompt", command=self.load_prompt)
        self.load_button.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_prompt)
        self.submit_button.pack()

        self.play_button = tk.Button(self.root, text="Play Response", command=self.play_response)
        self.play_button.pack()
        
        self.reset_button = tk.Button(self.root, text="Reset History", command=self.reset_history)
        self.reset_button.pack(pady=5)

    def reset_history(self):
        # Reset the conversation history
        if hasattr(self, 'model_response_generator') and hasattr(self.model_response_generator, 'response_generator'):
            self.model_response_generator.response_generator.conversation_history = []

        # Clear the text areas
        self.prompt_text.delete("1.0", tk.END)
        self.response_text.delete("1.0", tk.END)

        # Optionally re-initialize the model response generator if needed
        self.initialize_model_response_generator()


    # Previous code remains the same

    def load_prompt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                prompt = file.read()
                self.prompt_text.delete("1.0", tk.END)
                self.prompt_text.insert(tk.END, prompt)

    def start_speech(self):
        # Update the language of the SpeechToText instance
        selected_language = self.read_current_speech_language()
        self.speech_to_text.language = selected_language

        # Clear previous prompt and insert italicized message
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert(tk.END, "Say something to the microphone!")
        self.prompt_text.tag_add("italic", "1.0", "end")
        self.prompt_text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        
        # Start a new thread for speech recognition to avoid freezing the GUI
        threading.Thread(target=self.recognize_and_display_speech).start()

    def read_current_speech_language(self):
        # Read the current speech language from the combobox
        return self.speech_language_selector.get() if self.speech_language_selector.get() else 'es-US'


    def recognize_and_display_speech(self):
        # Perform speech recognition
        text = self.speech_to_text.recognize_speech()
        
        # Update the GUI with the recognized text
        self.update_prompt_text(text)

    def update_prompt_text(self, text):
        # Ensure this runs on the main thread
        if text:
            self.prompt_text.delete("1.0", tk.END)
            self.prompt_text.insert(tk.END, text)
        else:
            self.prompt_text.delete("1.0", tk.END)
            self.prompt_text.insert(tk.END, "Could not understand audio. Please try again.")
        self.root.after(1000, self.submit_prompt)

    def submit_prompt(self):
        selected_model = self.model_selector.get()
        if selected_model != self.current_model:
            self.initialize_model_response_generator()

        prompt = self.prompt_text.get("1.0", tk.END).strip()

        # Display an italicized 'Processing...' message
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, "Processing...")
        self.response_text.tag_add("italic", "1.0", "end")
        self.response_text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        
        
        # Hide the copy button when a new prompt is submitted
        self.copy_button.pack_forget()

        # Start a new thread for getting the model's response
        threading.Thread(target=self.process_and_display_response, args=(prompt,)).start()

    def process_and_display_response(self, prompt):
        # Get the model's response
        response = self.model_response_generator.get_response(prompt)

        # Update the response text and play the response on the main thread
        self.root.after(0, self.update_response_text, response)
        self.root.after(0, self.play_response)

    def update_response_text(self, text):
        # Update the response text with the model's response
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, text)
        self.response_text.tag_remove("italic", "1.0", "end")
        

        # Show the copy button when the response is updated
        self.copy_button.pack(side=tk.BOTTOM, pady=5)
 

    def play_response(self):
        # Move the audio playback to a new thread
        threading.Thread(target=self.play_response_audio).start()

    def play_response_audio(self):
        response = self.response_text.get("1.0", tk.END).strip()
        selected_voice = self.voice_selector.get()
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp3"
        output_file = os.path.join(self.temp_dir, filename)

        openai_voices = {'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'}
        if selected_voice in openai_voices:
            tts = OpenAITTS(api_key=os.getenv('OPENAI_API_KEY'))
            tts.convert_text_to_audio(response, output_file, voice=selected_voice)
        else:
            tts = EdgeTTS()
            tts.convert_text_to_audio(response, output_file, voice=selected_voice)

        # Play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
 
    def on_close(self):
        """ Function to clean up the temporary directory and close the window """
        # Attempt to delete the temporary directory
        # try:
        #     shutil.rmtree(self.temp_dir)
        # except OSError as e:
        #     print(f"Error deleting temporary files: {e.strerror}")

        # Destroy the main window
        self.root.destroy()


    def change_focus(self, event=None):
        self.root.focus_set()

    def run(self):
        self.root.mainloop()
        

    def get_model_kwargs(self, model_name):
        if 'gpt' in model_name:
            return read_kwargs_from_file("gpt_kwargs.txt")
        elif 'gemini' in model_name:
            return read_kwargs_from_file("gemini_kwargs.txt")
        return {}
    
def main():
    app = ChatGUI()
    app.run()

if __name__ == "__main__":
    main()


