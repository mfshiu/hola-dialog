import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Whisper device:{device}')
# whisper.DecodingOptions(language="zh")
whisper_model = whisper.load_model("small", device=device)

wave_path = '_input/voice-0725-0234-50.wav'
wave_path = '_input/voice-0725-0234-35.wav'
result = whisper_model.transcribe(wave_path)
print(f'result: {result}')

print(f'Finish test')
