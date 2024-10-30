import telebot

# Token do bot
api = "7950420239:AAE4aalvicMPv7_SFG26D0pMnLVbs1zVpkQ" #7950420239:AAE4aalvicMPv7_SFG26D0pMnLVbs1zVpkQ   7277223979:AAFL1497sJw25z6L-rXuH96wzTa6uGZPJhk
chat_id = "-1002467779183" # 6045775620 edu

# Inicializa o bot
bot = telebot.TeleBot(api)

def send_message(text):
    """Envia uma mensagem para o Telegram."""
    try:
        bot.send_message(chat_id, text)
        print(f"Mensagem enviada: {text}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
