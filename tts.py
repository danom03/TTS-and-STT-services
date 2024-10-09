import os
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()

filename = "output.wav"

def main():
    try:
        # Get user input for the text to be spoken
        user_text = input("Enter the text you want to convert to speech: ")

        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, {"text": user_text}, options)
        print(response.to_json(indent=4))

        print(f"Audio saved to {filename}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()