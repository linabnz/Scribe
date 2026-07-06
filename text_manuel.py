import sys
sys.path.insert(0, 'src')

from transcriber import transcribe_audio

result = transcribe_audio('audio_samples/audiotest.mp4')

print("--- Texte ---")
print(result.text)

print("\n--- Langue détectée ---")
print(result.language)

print("\n--- Durée ---")
print(result.duration)

print("\n--- Segments (horodatage) ---")
for segment in result.segments:
    print(segment)