import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("voice.ogg", 'wb') as new_file:
        new_file.write(downloaded_file)

    sound = AudioSegment.from_ogg("voice.ogg")
    sound.export("voice.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            bot.reply_to(message, "Ты сказал: " + text)
        except:
            bot.reply_to(message, "Не удалось распознать речь.")

bot.polling()
