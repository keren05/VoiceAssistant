#IMDbPY is a Python package that scrapes IMDb.
from imdb import IMDb

import speech_recognition as sr
import pyttsx3
from transformers import pipeline
import time
import requests
class FreeVoiceAssistant:
    def __init__(self):
        self.ia = IMDb()  # Initialize IMDbPY object
        self.recognizer = sr.Recognizer()

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

        # Initialize text generation model
        self.generator = pipeline('text-generation', model='gpt2')

        # Conversation history
        self.conversation_history = []
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {0}".format(e))
                return None

    def speak(self, text):
        print("AI:", text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def generate_response(self, prompt):
        # If the user asks for a movie recommendation, fetch it from TMDb
        if "recommend a movie" in prompt.lower():
            return self.get_movie_recommendation()
        else:
            # Otherwise, use GPT-2 for text generation
            context = " ".join(self.conversation_history[-3:] + [prompt])
            response = self.generator(context, max_length=500, num_return_sequences=1)
            return response[0]['generated_text'].split(prompt)[-1].strip()
    def get_movie_recommendation(self):
        # Get top 5 movies from IMDb's top 250 list
        top_movies = self.ia.get_top50_movies()
        if top_movies:
            top_movie = top_movies[0]  # Select the first movie
            title = top_movie['title']
            year = top_movie['year']
            return f"I recommend '{title}' from {year}."
        else:
            return "I couldn't find any recommendations."


    def run(self):
        self.speak("Hello! I'm your movie recommender assistant. How can I help you?")

        while True:
            try:
                # Listen for user input
                user_input = self.listen()

                if user_input:
                    # Add to conversation history
                    self.conversation_history.append(user_input)

                    # Generate response
                    response = self.generate_response(user_input)

                    # Add response to history
                    self.conversation_history.append(response)

                    # Speak response
                    self.speak(response)

                time.sleep(0.1)  # Small delay to prevent high CPU usage

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue


if __name__ == "__main__":
    # Install required packages
    """
    pip install SpeechRecognition
    pip install pyttsx3
    pip install pyaudio
    pip install transformers
    pip install torch
    pip install requests
    """

    assistant = FreeVoiceAssistant()
    assistant.run()