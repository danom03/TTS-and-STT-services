import assemblyai as aai
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
# from openai import OpenAI
from mistralai import Mistral
import os
from dotenv import load_dotenv


load_dotenv()

class AI_Assisstant:
    def __init__(self):
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")
        # openai_api_key = os.getenv("OPEN_AI_API_KEY")
        mistral_api_key = os.getenv("MISTRAIL_API_KEY")
        # self.openai_client = OpenAI(api_key=openai_api_key)
        self.mistral_client = Mistral(api_key=mistral_api_key)
        
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
        self.transcriber = None
        
        # Prompt
        self.full_transcript = [{
            "role":"system","content":"You are a receptionist at a dental clinic"
        }]
     
    
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # print("Session ID:", session_opened.session_id)
        return

    def on_data(self,transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
           # print(transcript.text, end="\r\n")
           self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self,error: aai.RealtimeError):
        # print("An error occured:", error)
        return


    def on_close(self):
        # print("Closing Session")
        return
       
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(sample_rate=16000,on_data=self.on_data,
                                                   on_error = self.on_error,
                                                   on_open = self.on_open,
                                                   on_close = self.on_close,
                                                   end_utterance_silence_threshold = 1000)
        
        self.transcriber.connect()
        microphone_stream = aai.extrax.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)
        
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None
            
    def generate_ai_response(self, transcript):
        
        self.stop_transcription()
        
        self.full_transcript.append({"role":"user","content":transcript.text})
        print(f"\nPatient:{transcript.text}",end="\r\n")
        response = self.mistral_client.chat.completions.create(model="mistral-large-latest",messages=self.full_transcript)
        
        ai_response = response.choices[0].message.content
        
        self.generate_audio(ai_response)
        
        self.start_transcription()
        
    def generate_audio(self,text):
        self.full_transcript.append({"role":"assisstant","content":text})
        print(f"\nAI Receptionist: {text}")
        
        #audio_stream = generate(api_key = self.elevenlabs_api_key,text = text,voice = "Rachel",stream = True)
        
        client = ElevenLabs(api_key=self.elevenlabs_api_key)
        audio_stream = client.generate(text=text,voice = "Rachel",stream = True)
        
        stream(audio_stream)
        
        
greeting = "Thank you for calling Dental Clinic. My name is Sam. How can I assisst you?"

ai_assisstant = AI_Assisstant()
ai_assisstant.generate_audio(greeting)
ai_assisstant.start_transcription()