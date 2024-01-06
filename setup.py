from setuptools import setup, find_packages

setup(
    name='VoiceGPT-Chat',
    version='1.0.0',
    author='Erick Eduardo Ramirez Torres',
    author_email='erickeduardoramireztorres@gmail.com',
    description='VoiceGPT-Chat provides a GUI for interactive conversations with GPT models using voice input and output.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eramireztorres/VoiceGPT-Chat',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pygame==2.5.2',
        'openai==1.6.1',
        'pydub==0.25.1',
        'google-ai-generativelanguage==0.4.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
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
            'voicegpt-chat=src.chat_gui:main',
        ],
    },
)
