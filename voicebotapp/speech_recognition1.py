

import os
import azure.cognitiveservices.speech as speechsdk

SPEECH_KEY="f1ffa1eaaa674d92931a17ed09ac4094"
SPEECH_REGION="eastus2"

def recognize_from_microphone():
    import os
    import azure.cognitiveservices.speech as speechsdk
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription='f1ffa1eaaa674d92931a17ed09ac4094', region='eastus2')
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text=print("{}".format(speech_recognition_result.text))

        return text
    else:
        return None

    #if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
     #   print("{}".format(speech_recognition_result.text))
        
      #  text=print("{}".format(speech_recognition_result.text))
        

    #elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
     #   print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    #elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    #    cancellation_details = speech_recognition_result.cancellation_details
    #    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    #    if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #        print("Error details: {}".format(cancellation_details.error_details))
    #        print("Did you set the speech resource key and region values?")

recognize_from_microphone()