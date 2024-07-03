import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
    
class AI_Assistant:
    def __init__(self):
        aai.settings.api_key = "API-KEY"
        self.openai_client = OpenAI(api_key= "API-KEY")
        self.elevenlabs_api_key = "API-KEY"
        self.transcriber = None
        #prompt
        self.full_transcript = [
            {"role":"system", "content":"you are a receptonist at dental clinic.Be resourceful and efficient"}
        ]
   #### step2 : real-transcription with assembly AI  #####

def start_transcription(self):
    self.transcriber = aai.RealtimeTranscriber(
    sample_rate = 16000,
    on_data = self.on_data,
    on_error = self.on_error,
    on_open = self.on_open,
    on_close = self.on_close,
    end_utterance_silence_threshold = 1000
    )
    self.transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
    self.transcriber.stream(microphone_stream)
def stop_transcription(self):
    if self.transciber:
        self.transcriber.close()
        self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return


    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self, error: aai.RealtimeError):
        print("An error occured:", error)
        return


    def on_close(self):
        #print("Closing Session")
        return
####### step 3: Pass real-time transcript to OPENAI #####
 
    def generate_ai_response(self, transcript):
        self.stop_transcription()
        self.full_transcript.append({"role":"user","content": transcript.text})
        print(f"\nPatient:{transcript.text}", end="\r\n")
        response = self.openai_client.chat.completion(
            model ="gpt_3.5-turbo",
            messages = self.full_transcript
        )
        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)

        self.start_transcription()
########## step 4: Generate audio with elevenlabs #####

    def generate_audio(self, text):

        self.full_transcript.append({"role":"assistant","content": text})
        print(f"\nAI Receptionist: {text}")

        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = "rachel",
            stream = True
        )

        stream(audio_stream)

    greeting = "Thank you for calling Vancouver dental clinic.  My name is JAAT, How may I assist you?"
    ai_assistant = AI_Assistant
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()