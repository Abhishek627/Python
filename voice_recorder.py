import speech_recognition as sr
def voice_recorder():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording...")
        r.energy_threshold = 100
        r.pause_threshold = 3
        audio = r.listen(source)

        try:
            print("Recognizing...")
            speech = r.recognize_google(audio)
            print("Recorded successfully!")

        except Exception as e:
            print("Not clear")

        with open("recordedaudio.wav", "wb") as f:
            f.write(audio.get_wav_data())



if __name__ == "__main__":
    voice_recorder()