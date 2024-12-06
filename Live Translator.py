import speech_recognition as sr
import warnings
from googletrans import Translator
import datetime
import threading



# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")



def get_microphone_input(language):
    """
    Capture audio from the microphone and transcribe using Whisper
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        # Listen for audio from the source Microphone
        audio = r.listen(source)

        try:
            # Return the audio 
            return r.recognize_whisper(audio, language=language)

        except sr.UnknownValueError:
            print("Whisper could not understand the audio.")
            return None

        except sr.RequestError as e:
            print(f"Could not request results from Whisper; {e}")
            return None



def translate_text(text, origin_language, target_language):
    """
    Translate text from one language to another
    """
    # Create a Translator object
    translator = Translator()

    # Get the translation given using the object created before
    return translator.translate(text, src=origin_language, dest=target_language).text



def log_translation(original, translation):
    """
    Log the translation to a file with a timestamp
    """

    # Store current time
    current_time = datetime.datetime.now()

    # Create the text to append to the file
    text = f"""
===== {current_time.day}/{current_time.month}/{current_time.year} {current_time.hour}:{current_time.minute}:{current_time.second} =====
{SOURCE_LANGUAGE} : {original}
{TARGET_LANGUAGE} : {translation}
==============================

"""
    # Open the file in append mode and write to it
    with open('log.txt', 'a', encoding='UTF-8') as f:
        f.write(text)



def threaded_log(original, translation):
    """
    Write log using a separate thread to not stop the speech recognition
    """
    # Create the thread using lambda
    thread = threading.Thread(
        target=lambda: log_translation(original, translation)
    )
    # Start the thread
    thread.start()



SOURCE_LANGUAGE = 'ru'
TARGET_LANGUAGE = 'en'


# Main
if __name__ == '__main__':

    print(f"Source Language: {SOURCE_LANGUAGE}")
    print(f"Translation Language: {TARGET_LANGUAGE}")

    print("Press Ctrl+C to exit.")

    # Infinite loop
    while True:

        try:

            # Get audio from microphone
            speech = get_microphone_input(SOURCE_LANGUAGE)

            # Check whether if there's audio
            if speech:

                # Store Translation
                translation = translate_text(speech, SOURCE_LANGUAGE, TARGET_LANGUAGE)

                # Show The original
                print(f"Original (in {SOURCE_LANGUAGE}): {speech}")
                print(f"Translated (to {TARGET_LANGUAGE}): {translation}")

                # Log translation using threading
                threaded_log(speech, translation)

        except KeyboardInterrupt:
            print("\nExiting.")
            break

        except Exception as e:
            print(f"Something went wrong: {e}")
