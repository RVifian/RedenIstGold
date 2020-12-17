from resemblyzer import preprocess_wav, VoiceEncoder
from demo_utils_1min import *
from pathlib import Path


# Source for the interview: https://www.srf.ch/play/tv/arena/video/abstimmungs-arena-zur-konzernverantwortungsinitiative?urn=urn:srf:video:a1a54687-eae7-4579-9735-07a1a4227899

# 15 min Verison:
# wav_fpath = Path("audio_data", "Abstimmungs-Arena» zur Konzernverantwortungsinitiative-a1a54687-eae7-4579-9735-07a1a4227899_15min.wav")

# 1 min Verison:
wav_fpath = Path(
    "audio_data", "Abstimmungs-Arena» zur Konzernverantwortungsinitiative-a1a54687-eae7-4579-9735-07a1a4227899_1min.wav")
wav = preprocess_wav(wav_fpath)

# Cut some segments from single speakers as reference audio
# 15 min Version:
# segments = [[113, 140], [34, 50], [190, 230], [873, 880], [764, 800], [672, 720]]
# speaker_names = ["Sandro Botz Moderator", "Backgroundinfo Sprecherin", "Karin Keller-Sutter, Bundesrätin", "Martin Landolt, Präsident BDP", "Gerhard Pfister, Präsident CVP", "Daniel Jositsch, Ständerat SP"]
# speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]

# Cut some segments from single speakers as reference audio
# 1 min Version:
segments = [[00, 11], [14, 30]]
speaker_names = ["Sandro Botz, Moderator", "Karin Keller-Sutter, Bundesrätin"]
speaker_wavs = [
    wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]


# Compare speaker embeds to the continuous embedding of the interview
# Derive a continuous embedding of the interview. We put a rate of 16, meaning that an
# embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker
# diarization, but it is not so useful for when you only need a summary embedding of the
# entire utterance. A rate of 2 would have been enough, but 16 is nice for the sake of the
# demonstration.
# We'll exceptionally force to run this on CPU, because it uses a lot of RAM and most GPUs
# won't have enough. There's a speed drawback, but it remains reasonable.
encoder = VoiceEncoder("cpu")
print("Running the continuous embedding on cpu, this might take a while...")
_, cont_embeds, wav_splits = encoder.embed_utterance(
    wav, return_partials=True, rate=16)


# Get the continuous similarity for every speaker. It amounts to a dot product between the
# embedding of the speaker and the continuous embedding of the interview
speaker_embeds = [encoder.embed_utterance(
    speaker_wav) for speaker_wav in speaker_wavs]
similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in
                   zip(speaker_names, speaker_embeds)}

# Print the amount of wav_splits
#number = 1
#for i in range(len(wav_splits)):
#    print(number)
#    number = number + 1

# Run the interactive demo
interactive_diarization(similarity_dict, wav, wav_splits)
