# VoiceGPT-Chat

VoiceGPT-Chat is an interactive chat application that enables users to communicate with GPT models using voice inputs and outputs. This tool combines the power of speech recognition, text-to-speech, and advanced language models to create a seamless conversational experience.

## Installation

VoiceGPT-Chat requires Python 3.6 or higher. To install VoiceGPT-Chat, follow these steps:

Make sure you use python 3.11 or higher.
Since PyPI is temporarily not accepting new user registrations, you can install VoiceGPT-chat directly from the source using the following steps:
1. Clone the GitHub repository:
```
git@github.com:eramireztorres/voicegpt-chat.git
cd voicegpt-chat
```
2. Install the package:
```
python setup.py install
```

This will install VoiceGPT-Chat along with its dependencies.

## Dependencies

Apart from the Python packages installed by default, this project also depends on `edge-tts` and  `google-generativeai`. 

To install these dependencies, run the following command:

```bash
pip install edge-tts
```

```bash
pip install google-generativeai
```

## Additional Requirement for Windows Users: PowerShell

VoiceGPT-Chat requires PowerShell to be installed on Windows systems for certain functionalities. Follow these steps to install and configure PowerShell:

1. **Checking PowerShell Version:**
   - First, check if you have PowerShell installed and its version. PowerShell 5.1 or higher is recommended for optimal compatibility.
   - Open a Command Prompt and type `powershell` followed by `$PSVersionTable.PSVersion`. This will display the PowerShell version.

2. **Installing or Updating PowerShell:**
   - If PowerShell is not installed or you need to update it, download the latest version from the [official PowerShell GitHub repository](https://github.com/PowerShell/PowerShell).
   - Choose the appropriate installer for your version of Windows (Windows 7/8/10/11).

3. **Installing PowerShell via Windows Features (Optional):**
   - For Windows 10 and later, PowerShell can also be installed via Windows Features.
   - Navigate to 'Control Panel' > 'Programs' > 'Turn Windows features on or off'.
   - Check the box for 'Windows PowerShell' and click 'OK'. Follow the prompts to complete the installation.

4. **Setting Execution Policy (If Required):**
   - Some PowerShell scripts require setting the execution policy.
   - Open PowerShell as an administrator and run `Set-ExecutionPolicy RemoteSigned` or a policy level that suits your security needs.

5. **Verifying Installation:**
   - After installation, verify by opening PowerShell and typing `$PSVersionTable.PSVersion`.

Please ensure that PowerShell is properly installed and configured on your Windows system to utilize all features of PyVideoCreator.


## Usage
To use VoiceGPT-Chat, follow these steps:

    Start the GUI:
    
```bash 
voicegpt-chat
```

1.  Select the desired voice and GPT model from the dropdown menus in the application.

2.  Press the "Start Speech" button or the space bar to start recording your voice.

3.  Speak into the microphone and wait for the speech to be transcribed and processed.

4.  The application will display and read out the GPT model's response.

Remember to check your microphone and speaker settings to ensure they are correctly configured.

## License

VoiceGPT-Chat is licensed under the MIT License.