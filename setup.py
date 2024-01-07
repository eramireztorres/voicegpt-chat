from setuptools import setup, find_packages

# Ensure that the README.md file exists and is accessible
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='VoiceGPT-Chat',
    version='1.0.0',
    author='Erick Eduardo Ramirez Torres',
    author_email='erickeduardoramireztorres@gmail.com',
    description='VoiceGPT-Chat provides a GUI for interactive conversations with GPT models using voice input and output.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eramireztorres/VoiceGPT-Chat',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'SpeechRecognition',
        'pygame==2.5.2',
        'openai==1.6.1',
        'pydub==0.25.1',
        'PyAudio==0.2.14'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat'
    ],
    python_requires='>=3.6',
    keywords='gpt, chatbot, voice recognition, text-to-speech, speech-to-text, AI, artificial intelligence',
    entry_points={
        'console_scripts': [
            'voicegpt-chat=voicegpt_chat.chat_gui:main',
        ],
    },
)
