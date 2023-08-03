import speech_recognition as sr
import openai

openai.api_key = "your_api_key_here"

def listen_for_quote():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source, timeout=500)
                text = recognizer.recognize_google(audio)

                if "quote me" in text.lower():
                    print("Listening for a quote...")
                    quote_text = recognize_quote(recognizer, source)
                    if quote_text:
                        print("You said:", quote_text)
                        generate_response(quote_text)
                elif "stop listening" in text.lower():
                    print("Stopped listening.")
                    break
                else:
                    print("You said:", text)

            except sr.UnknownValueError:
                print("Sorry, I could not understand you.")
            except sr.RequestError:
                print("There was an issue with the Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("Timeout. Listening for a command...")
                pass
            except KeyboardInterrupt:
                print("Listening interrupted.")
                break

def recognize_quote(recognizer, source):
    recognizer.pause_threshold = 1
    audio = recognizer.listen(source, phrase_time_limit=100)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't capture the quote."
    except sr.RequestError:
        return "There was an issue with the Google Speech Recognition service."

def generate_response(quote_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=quote_text,
        max_tokens=150,
        stop=None,
    )
    print("GPT-3 Response:", response.choices[0].text.strip())

if __name__ == "__main__":
    listen_for_quote()
