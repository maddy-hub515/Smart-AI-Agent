import pyttsx3

def speak_text_offline(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)     # Speed of speech (default ~200)
        engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Choose voice [0] for male, [1] for female (may vary by OS)
        
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"🔊 Text-to-speech failed: {e}")