import whisper

class SpeechToText:
    def __init__(self, model_name='tiny'):
        self.model = whisper.load_model(model_name)

    def __call__(self, audio_file):
        result = self.model.transcribe(audio_file)
        return result['text']
    
if __name__ == '__main__':
    stt = SpeechToText()
    text = stt.transcribe('RAG\\audio\\hello.wav')
    print(text)