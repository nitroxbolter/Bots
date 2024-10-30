import websocket
import json
from datetime import datetime
import telebot
import time  # Importando time para usar no delay de reconexão

# Configurações do bot
api = "7277223979:AAFL1497sJw25z6L-rXuH96wzTa6uGZPJhk"  # Token do bot
chat_id = "6045775620"  # ID do chat

bot = telebot.TeleBot(api)

# Variáveis globais
buffer = ""
processed_ids = set()
resultado = []
check_resultado = []
analise_sinal = False
cor_sinal = ''
historico_resultados = []  # Inicializa a lista para armazenar resultados
previous_result = None  # Variável para armazenar o resultado anterior
entrada = 0  # Inicializa a variável de entrada para martingale
max_gale = 2  # Defina o número máximo de martingales que você deseja permitir
ultimo_resultado = None  # Variável para rastrear o último resultado

def on_message(ws, message):
    global buffer, historico_resultados  # Declare historico_resultados como global
    buffer += message
    try:
        while buffer:
            if buffer.startswith("42"):
                data = json.loads(buffer[2:])  # Ignora os dois primeiros caracteres
                buffer = ""  # Limpa o buffer após processar a mensagem

                if isinstance(data, list) and len(data) > 1:
                    informacoes_relevantes = extract_relevant_info(data)
                    if informacoes_relevantes:
                        resultado = informacoes_relevantes['roll']
                        global previous_result
                        if resultado != previous_result:
                            previous_result = resultado  # Atualiza o resultado anterior
                            estrategy(resultado, minute)  # Chama a função de estratégia

            else:
                buffer = ""  # Limpa o buffer se a mensagem não começar com "42"
                break
    except Exception as e:
        print(f"Erro inesperado ao processar a mensagem: {e}")

def extract_relevant_info(data):
    try:
        payload = data[1]['payload']
        if payload.get("status") != "rolling":
            return None

        created_at = payload.get("created_at")
        created_at_dt = datetime.fromisoformat(created_at[:-1])  # Remove o 'Z'
        minute = created_at_dt.minute

        roll = payload.get("roll", [])
        if isinstance(roll, int):
            roll = [roll]
        
        informacoes_relevantes = {
            "id": payload.get("id"),
            "color": payload.get("color"),
            "roll": roll,
            "minute": minute,
            "created_at": created_at_dt
        }
        return informacoes_relevantes
    except (KeyError, IndexError) as e:
        print(f"Erro ao extrair informações: {e}")
        return None

def estrategy(resultado, minute):
    global analise_sinal
    global cor_sinal
    global historico_resultados
    global first_result
    global second_result
    
    # Aqui você pode adicionar o código que utiliza resultado e minute
    print(f"Resultado: {resultado}, Minute: {minute}")
    # Implementação da lógica da estratégia


    cores = []
    for x in resultado:
        if x >= 1 and x <= 7:
            color = 'V'  # Vermelho
            cores.append(color)
        elif x >= 8 and x <= 14:
            color = 'P'  # Preto
            cores.append(color)
        else:
            color = 'B'  # Branco
            cores.append(color)

    historico_resultados.extend(cores)

    # Mantém apenas os últimos 10 resultados
    if len(historico_resultados) > 10:
        historico_resultados = historico_resultados[-10:]

    print(', '.join(historico_resultados))

    # Sinal 00: condições específicas
    if minute == 24:
        if first_result is None:
            # Armazena o primeiro resultado
            first_result = cores[-1] if cores else None
            print(f'Primeiro resultado armazenado: {first_result}')
        elif second_result is None:
            # Armazena o segundo resultado
            second_result = cores[-1] if cores else None
            print(f'Segundo resultado armazenado: {second_result}')

            # Compara o primeiro e o segundo resultados para o sinal 00
            if first_result and second_result:
                if second_result == 'P':
                    cor_sinal = '⚫️'
                    padrao = '🥷🏽Sinal 00: Apostar no V🥷🏽'  # Sinal 00
                    enviar_sinal(cor_sinal, padrao)
                    analise_sinal = True
                    print('Sinal enviado: 🥷🏽Sinal 00: Apostar no V🥷🏽')
                elif second_result == 'V':
                    cor_sinal = '⚫️'
                    padrao = '🥷🏽Sinal 00: Apostar no P🥷🏽'  # Sinal 00
                    enviar_sinal(cor_sinal, padrao)
                    analise_sinal = True
                    print('Sinal enviado: 🥷🏽Sinal 00: Apostar no P🥷🏽')

            # Limpa as variáveis para aguardar o próximo par de resultados
            first_result = None
            second_result = None

    # Lógica para outros sinais (Samurai, Sniper e King)
    if analise_sinal:
        correcao(historico_resultados, cor_sinal)  # Chama a função de correção se necessário
    else:
        if len(historico_resultados) >= 2 and historico_resultados[-2:] == ['P', 'V']:
            cor_sinal = '⚫️'
            padrao = '🥷🏽Samurai🥷🏽'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('Sinal enviado: 🥷🏽Samurai🥷🏽')

        # Adiciona o padrão Sniper: ao sair um B, apostar no V
        if len(historico_resultados) > 0 and historico_resultados[-1] == 'B':
            cor_sinal = '🛑'
            padrao = '🧭Sniper🧭'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('Sinal enviado: 🧭Sniper🧭')

        # Verifica o padrão King: sequência V, V, P, P
        if len(historico_resultados) >= 4 and historico_resultados[-4:] == ['V', 'V', 'P', 'P']:
            cor_sinal = '🛑'
            padrao = '👑King👑'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('Sinal enviado: 👑King👑')


def enviar_sinal(cor, padrao):
    mensagem = f'''
🚨 Sinal encontrado 🚨

⏯️ Padrão: {padrao}

💶 Entrar no {cor}

🦾 Proteger no ⚪️

🐓 2 martingale: (opcional)
'''
    bot.send_message(chat_id, text=mensagem)
    print(f'Mensagem enviada para o Telegram: {mensagem}')  # Log para depuração

    # Após o envio do sinal, ativa a análise da correção
    correcao(historico_resultados, cor_sinal)

def correcao(results, color):
    global analise_sinal, ultimo_resultado, first_result, second_result
    if not analise_sinal:  # Só permite correção se estiver em análise
        return

    current_result = results[0:1]

    # Correção para o sinal 00
    if first_result is not None and second_result is not None:
        if second_result == 'P':
            color = '⚫️'  # Apostar no V
        elif second_result == 'V':
            color = '🛑'  # Apostar no P

    # Lógica existente para correção
    if current_result == ['P'] and color == '⚫️':
        if ultimo_resultado != "win":
            win()
            ultimo_resultado = "win"
            reset()
        return
    elif current_result == ['V'] and color == '🛑':
        if ultimo_resultado != "win":
            win()
            ultimo_resultado = "win"
            reset()
        return
    elif current_result == ['P'] and color == '🛑':
        if ultimo_resultado != "loss":
            martingale()
            ultimo_resultado = "loss"
        return
    elif current_result == ['V'] and color == '⚫️':
        if ultimo_resultado != "loss":
            martingale()
            ultimo_resultado = "loss"
        return
    elif current_result == ['B']:
        if ultimo_resultado != "win":
            win()
            ultimo_resultado = "win"
            reset()

def win():
    bot.send_message(chat_id, text="✅")  # Enviar esticker: bot.send_sticker(chat_id, sticker="ID_DO_STICKER")
    return

def loss():
    bot.send_message(chat_id, text="❌")
    return

def reset():
    global analise_sinal, entrada, ultimo_resultado, first_result, second_result
    entrada = 0
    analise_sinal = False
    ultimo_resultado = None  # Reseta o último resultado
    first_result = None  # Reseta o primeiro resultado
    second_result = None  # Reseta o segundo resultado
    return

def martingale():
    global entrada
    entrada += 1
    if entrada <= max_gale:
        bot.send_message(chat_id, text=f"⚠️ Gale {entrada} ⚠️")
    else:
        loss()
        reset()
    return


def on_error(ws, error):
    print(f"Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    while True:
        try:
            time.sleep(5)  # Espera 5 segundos antes de tentar reconectar
            start_websocket()  # Tenta reiniciar a conexão
            break  # Se a reconexão for bem-sucedida, sai do loop
        except Exception as e:
            print(f"Erro ao tentar reconectar: {e}")

def on_open(ws):
    subscribe_message = "420" + json.dumps(["cmd", {
        "id": "subscribe",
        "payload": {
            "room": "double_room_1"
        }
    }])
    ws.send(subscribe_message)

def start_websocket():
    websocket_url = "wss://api-gaming.blaze1.space/replication/?EIO=3&transport=websocket"
    ws = websocket.WebSocketApp(websocket_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    print("Iniciando o WebSocket...")
    start_websocket()
