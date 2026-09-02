import librosa
import torch

from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification
)

from pydub import AudioSegment

import os


MODEL_NAME = (
    "garystafford/"
    "wav2vec2-deepfake-voice-detector"
)


print(
    "Loading AI voice detection model..."
)


feature_extractor = (
    AutoFeatureExtractor.from_pretrained(
        MODEL_NAME
    )
)


model = (
    AutoModelForAudioClassification
    .from_pretrained(
        MODEL_NAME
    )
)


model.eval()


def predict_voice(file_path):

    wav_path = (
        file_path + "_converted.wav"
    )


    try:

        print(
            "Converting audio to WAV..."
        )


        audio_file = (
            AudioSegment.from_file(
                file_path
            )
        )


        audio_file.export(

            wav_path,

            format="wav"

        )


        print(
            "Loading converted audio..."
        )


        audio, sample_rate = (
            librosa.load(

                wav_path,

                sr=16000,

                mono=True

            )
        )


        print(
            "Preparing audio for AI model..."
        )


        inputs = (
            feature_extractor(

                audio,

                sampling_rate=16000,

                return_tensors="pt",

                padding=True

            )
        )


        print(
            "Analyzing voice..."
        )


        with torch.no_grad():

            outputs = model(
                **inputs
            )


        probabilities = (
            torch.softmax(

                outputs.logits,

                dim=-1

            )[0]
        )


        labels = (
            model.config.id2label
        )


        result = {

            labels[i]:

            round(

                probabilities[i]
                .item() * 100,

                2

            )

            for i in range(
                len(probabilities)
            )

        }


        print(
            "Model result:",
            result
        )


        fake_probability = 0


        for (
            label,
            probability

        ) in result.items():


            label_lower = (
                label.lower()
            )


            if (

                "fake"
                in label_lower

                or

                "spoof"
                in label_lower

                or

                "deepfake"
                in label_lower

            ):

                fake_probability = (
                    probability
                )


        return {

            "ai_generated_probability":

            fake_probability,


            "model_status":

            "Pretrained AI voice detection model",


            "all_predictions":

            result

        }


    finally:

        if os.path.exists(
            wav_path
        ):

            os.remove(
                wav_path
            )