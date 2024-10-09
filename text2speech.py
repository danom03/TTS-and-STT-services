import os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf


from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()

def Text2Speech(SPEAK_OPTIONS,filename):
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        # print(response.to_json(indent=4))
        
        data, fs = sf.read("output.wav", dtype='float32')
        sd.play(data, fs)
        sd.wait()
        
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    Text2Speech({"text": "Hello, how can I help you today?"},'output.wav')