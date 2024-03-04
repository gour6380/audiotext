#Importing necessary libraries
import json
import os
from .audio import get_text
import time
from concurrent.futures import ThreadPoolExecutor

ALLOWED_EXTENSIONS = {'wav', 'mp3'}

ALLOWED_LANGLUAGE_CODE = set(["af-ZA","sq-AL","am-ET","ar-DZ","ar-BH","ar-EG","ar-IQ","ar-IL","ar-JO","ar-KW","ar-LB","ar-MR","ar-MA","ar-OM","ar-QA","ar-SA","ar-PS","ar-TN","ar-AE","ar-YE","hy-AM","az-AZ","eu-ES","bn-BD","bn-IN","bs-BA","bg-BG","my-MM","ca-ES","yue-Hant-HK","zh (cmn-Hans-CN)","zh-TW (cmn-Hant-TW)","hr-HR","cs-CZ","da-DK","nl-BE","nl-NL","en-AU","en-CA","en-GH","en-HK","en-IN","en-IE","en-KE","en-NZ","en-NG","en-PK","en-PH","en-SG","en-ZA","en-TZ","en-GB","en-US","et-EE","fil-PH","fi-FI","fr-BE","fr-CA","fr-FR","fr-CH","gl-ES","ka-GE","de-AT","de-DE","de-CH","el-GR","gu-IN","iw-IL","hi-IN","hu-HU","is-IS","id-ID","it-IT","it-CH","ja-JP","jv-ID","kn-IN","kk-KZ","km-KH","rw-RW","ko-KR","lo-LA","lv-LV","lt-LT","mk-MK","ms-MY","ml-IN","mr-IN","mn-MN","ne-NP","no-NO","fa-IR","pl-PL","pt-BR","pt-PT","pa-Guru-IN","ro-RO","ru-RU","sr-RS","si-LK","sk-SK","sl-SI","st-ZA","es-AR","es-BO","es-CL","es-CO","es-CR","es-DO","es-EC","es-SV","es-GT","es-HN","es-MX","es-NI","es-PA","es-PY","es-PE","es-PR","es-ES","es-US","es-UY","es-VE","su-ID","sw-KE","sw-TZ","ss-Latn-ZA","sv-SE","ta-IN","ta-MY","ta-SG","ta-LK","te-IN","th-TH","ts-ZA","tn-Latn-ZA","tr-TR","uk-UA","ur-IN","ur-PK","uz-UZ","ve-ZA","vi-VN","xh-ZA","zu-ZA"])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def main(filename,enable_speaker_diarization, diarization_speaker_count, language_code):
	print(enable_speaker_diarization)

	#checking file name
	if not isinstance(filename, str):
		return json.dumps({"success": False, "text": "filename should be a string"})
	if not allowed_file(filename):
		return json.dumps({"success": False, "text": f"This file extension is not supported only {ALLOWED_EXTENSIONS} supported"})
	if not os.path.exists(filename):
		return json.dumps({"success" :False, "text": f"The file '{filename}' does not exist."})

	if not isinstance(enable_speaker_diarization, bool):
		return json.dumps({"success": False, "text": "Only Boolean values allowed for enable_speaker_diarization"})
	if not isinstance(diarization_speaker_count, int):
		return json.dumps({"success": False, "text": "Only Int values allowed for diarization_speaker_count"})
	if not isinstance(language_code, str):
		return json.dumps({"success": False, "text": "Only String values allowed for language_code"})
	if language_code not in ALLOWED_LANGLUAGE_CODE:
		return json.dumps({"success": False, "text": f"This Language is not supported only {ALLOWED_LANGLUAGE_CODE} supported"})

	if diarization_speaker_count < 0:
		return json.dumps({"success": False, "text": "Only Positive Int values allowed for diarization_speaker_count"})
	if  not enable_speaker_diarization and diarization_speaker_count > 1:
		return json.dumps({"success": False, "text": "If enable_speaker_diarization is False then diarization_speaker_count should be 1"})

	if not enable_speaker_diarization:
		enable_speaker_diarization = True
	# Create a ThreadPoolExecutor
	with ThreadPoolExecutor(max_workers=1) as executor:
		# Submit the function to the thread pool
		future = executor.submit(get_text, filename, enable_speaker_diarization, diarization_speaker_count,language_code)
		# Retrieve the result
		return future.result()

if __name__ == '__main__':
	main(["client/sample.mp3", "client/conversation_audio.wav"],[False ,True],[1,2],["en-GB","en-IN"])







