from gtts import gTTS
import os

# Text to be converted to speech (in Malayalam)
text = "ഐ.എസ് . ആർ .ഓ  ഇൽ നിന്ന് റാം സിങ് ആവശ്യപ്പെട്ട ഗാനം.... എന്ത് ഭംഗി നിന്നെ കാണാൻ പുള്ളീടെ ഓമലാളേ......  "

# Language in which you want to convert (Malayalam)
language = 'ml'

# Creating a gTTS object
speech = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a mp3 file
speech.save("malayalam_text_to_speech.mp3")

# Playing the converted file
# os.system("start malayalam_text_to_speech.mp3")  # For Windows
os.system("xdg-open malayalam_text_to_speech.mp3")  # For Linux
# os.system("open malayalam_text_to_speech.mp3")  # For macOS
