
import random
import datetime
import requests
import pickle

# Load model & vectorizer
model = pickle.load(open("intent_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Fungsi untuk menyimpan log percakapan
def save_conversation_log(user_input, bot_response):
    with open("conversation_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - User: {user_input} - Bot: {bot_response}\n")

# API cuaca
API_KEY = "b46e6fad8459cedb9b6d6bc6b40bc4d4"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city="Semarang"):
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"]
        description = weather_data["description"]
        return f"Suhu di {city}: {temperature}°C dengan cuaca {description}."
    else:
        return "Maaf, saya tidak bisa mendapatkan data cuaca saat ini."

intents = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["hi", "hello", "hey", "halo", "greetings"],
            "responses": ["Halo!", "Hai, ada yang bisa saya bantu?", "Hai juga!"]
        },
        {
            "tag": "goodbye",
            "patterns": ["bye", "see you", "goodbye", "sampai jumpa"],
            "responses": ["Sampai jumpa!", "Bye bye!", "Semoga harimu menyenangkan!"]
        },
        {
            "tag": "thanks",
            "patterns": ["thanks", "thank you", "terima kasih"],
            "responses": ["Sama-sama!", "Senang bisa membantu!", "Kapan saja!"]
        },
        {
            "tag": "time",
            "patterns": ["what time is it", "jam berapa", "time", "waktu sekarang"],
            "responses": [
                "Saat ini adalah: " + datetime.datetime.now().strftime("%H:%M:%S"),
                "Sekarang waktu: " + datetime.datetime.now().strftime("%H:%M:%S")
            ]
        },
        {
            "tag": "weather",
            "patterns": ["what's the weather like", "weather", "how's the weather", "cuaca", "suhu"],
            "responses": [
                get_weather("Semarang"),
                get_weather("Jakarta"),
                get_weather("Bandung")
            ]
        },
        {
            "tag": "joke",
            "patterns": ["tell me a joke", "joke", "give me a joke"],
            "responses": [
                "Kenapa komputer selalu dingin? Karena sering di-reboot!",
                "Kenapa orang suka main game? Karena mereka selalu punya level yang lebih tinggi!",
                "Apa bedanya programmer dengan pemandu wisata? Programmer menemukan bug, pemandu wisata menemukan tempat wisata!"
            ]
        },
        {
            "tag": "date",
            "patterns": ["tanggal berapa", "hari ini tanggal berapa", "what's the date", "tanggal"],
            "responses": [
                "Hari ini adalah " + datetime.datetime.now().strftime("%A, %d %B %Y"),
                "Sekarang tanggal: " + datetime.datetime.now().strftime("%d/%m/%Y")
            ]
        },
        {
            "tag": "fallback_funny",
            "patterns": ["kamu sedang apa", "lagi apa", "lagi ngapain", "kamu sibuk?"],
            "responses": [
                "Lagi nemenin kamu nih 😄",
                "Ngobrol sama kamu dong!",
                "Nunggu kamu nanya sesuatu 😁",
                "Bot juga butuh cinta, lho~"
            ]
        }
    ]
}

# Fungsi klasifikasi intent
def classify_intent(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# Fungsi response baru
def get_response(user_input):
    intent_tag = classify_intent(user_input)
    for intent in intents['intents']:
        if intent['tag'] == intent_tag:
            response = random.choice(intent['responses'])
            save_conversation_log(user_input, response)
            return response

    fallback = "Maaf, saya belum paham maksudnya."
    save_conversation_log(user_input, fallback)
    return fallback
