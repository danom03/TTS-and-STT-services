import xml.etree.ElementTree as ET
from TTS.api import TTS

def process_ssml(ssml_string):
    root = ET.fromstring(ssml_string)
    processed_text = []
    
    for element in root.iter():
        if element.tag == 'p':
            processed_text.append(element.text.strip() if element.text else '')
        elif element.tag == 'break':
            processed_text.append(f"[BREAK {element.attrib.get('time', '1s')}]")
        elif element.tag == 'emphasis':
            level = element.attrib.get('level', 'moderate')
            processed_text.append(f"[EMPHASIS {level}]{element.text}[/EMPHASIS]")
        elif element.tag == 'say-as':
            interpret_as = element.attrib.get('interpret-as', '')
            processed_text.append(f"[SAY-AS {interpret_as}]{element.text}[/SAY-AS]")
    
    return ' '.join(processed_text)

# Create a TTS instance
tts = TTS()

# List available models
print(tts.list_models())

model_name = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(model_name=model_name, progress_bar=False, gpu=False)


with open('ssml_file.xml', 'r') as file:
    ssml_content = file.read()


processed_text = process_ssml(ssml_content)


tts.tts_to_file(text=processed_text, file_path="output.wav")

print("Speech synthesis complete. Output saved as 'output.wav'.")