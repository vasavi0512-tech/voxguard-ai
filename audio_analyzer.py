import librosa


def analyze_audio(file_path):
    audio, sample_rate = librosa.load(file_path, sr=None)

    duration = librosa.get_duration(y=audio, sr=sample_rate)

    return {
        "duration_seconds": round(duration, 2),
        "sample_rate": sample_rate
    }