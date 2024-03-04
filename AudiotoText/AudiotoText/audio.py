import os
import json
import subprocess
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2.service_account import Credentials
from google.protobuf.json_format import MessageToDict, MessageToJson
import requests


def get_text(filename, enable_speaker_diarization, diarization_speaker_count, language_code):
    """Transcribe the given audio file with speaker diarization."""

    try:
        print("Get_text function is started")
        if filename.rsplit('.', 1)[1].lower() == "mp3":
            convert_mp3_to_wav(filename,filename.rsplit('.', 1)[0]+".wav")
            filename = filename.rsplit('.', 1)[0]+".wav"


        # Get credentials from environment variable
        credentials_raw = os.environ.get("GOOGLE_CLOUD_CREDENTIALS")
        credentials_json = json.loads(credentials_raw)
        credentials = Credentials.from_service_account_info(credentials_json)

        client = speech.SpeechClient(credentials=credentials)
        print("File opened")
        with open(filename, "rb") as audio_file:
            content = audio_file.read()
        print("Audio object created")
        audio = speech.RecognitionAudio(content=content)

        encoding = get_audio_encoding(filename)
        print("Config creating")
        config = speech.RecognitionConfig(
            encoding=encoding,
            #sample_rate_hertz=16000,
            language_code=language_code,
            enable_speaker_diarization=enable_speaker_diarization,
            diarization_speaker_count=diarization_speaker_count,  # Adjust this based on the number of speakers you expect
        )

        response = client.recognize(config=config, audio=audio)
        # response_json = type(response).to_json(response)

        print("Got response")
        prev_speaker = 0
        
        conversation = []
        current_speaker = None
        for result in response.results:
            for word_info in result.alternatives[0].words:
                speaker_tag = word_info.speaker_tag
                word = word_info.word

                if str(speaker_tag) != "0":
                    # Detect speaker change
                    if current_speaker != speaker_tag:
                        current_speaker = speaker_tag
                        conversation.append({"speaker": current_speaker, "text": word})
                    else:
                        conversation[-1]["text"] += " " + word

        return json.dumps({"success": True, "text": conversation})
    except Exception as e:
        return json.dumps({"success": False, "text": str(e)})


def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    print("Converting mp3 to wav file")
    cmd = [
        'ffmpeg',
        '-y',
        '-i', mp3_file_path,
        '-acodec', 'pcm_s16le',  # Set audio codec to pcm_s16le (Linear PCM)
        '-ac', '1',  # Set number of audio channels to 1 (mono)
        '-ar', '16000',  # Set audio sample rate to 16 kHz
        wav_file_path
    ]
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def get_audio_encoding(file_path):
    print("Getting audio encoding")
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        file_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    output = json.loads(result.stdout)

    # Fetching the codec name and bit depth
    codec_name = output['streams'][0]['codec_name']
    if 'bits_per_raw_sample' in output['streams'][0]:
        bit_depth = int(output['streams'][0]['bits_per_raw_sample'])
    else:
        bit_depth = None

    if codec_name == 'pcm_s16le':
        return speech.RecognitionConfig.AudioEncoding.LINEAR16
    elif codec_name == 'flac':
        # FLAC may be 16 or 24 bit
        return speech.RecognitionConfig.AudioEncoding.FLAC
    elif codec_name == 'mulaw':
        return speech.RecognitionConfig.AudioEncoding.MULAW
    elif codec_name == 'amr_nb':  # NB: Narrowband
        return speech.RecognitionConfig.AudioEncoding.AMR
    elif codec_name == 'amr_wb':  # WB: Wideband
        return speech.RecognitionConfig.AudioEncoding.AMR_WB
    else:
        return speech.RecognitionConfig.AudioEncoding.LINEAR16


if __name__=="__main__":
    print(get_text("conversation_audio.wav",True, 2, "en-US"))