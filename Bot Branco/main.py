import websocket
import json
import threading
import time
from monitor import process_message  # Importa a função de monitoramento
from bot import send_message  # Importando a função de envio de mensagens

def on_message(ws, message):
    """Callback para mensagens recebidas."""
    process_message(message)  # Processa a mensagem recebida

def on_error(ws, error):
    """Callback para erros."""
    print(f"Erro: {error}")  # Adicionando log de erro

def on_close(ws, close_status_code, close_msg):
    """Callback para fechamento da conexão.""" 

def on_open(ws):
    """Callback para conexão aberta.""" 
    subscribe_message = "420" + json.dumps(["cmd", {
        "id": "subscribe",
        "payload": {
            "room": "double_room_1"
        }
    }])
    ws.send(subscribe_message)

def start_websocket():
    """Inicia a conexão websocket e mantém o loop rodando.""" 
    websocket_url = "wss://api-gaming.blaze1.space/replication/?EIO=3&transport=websocket"
    ws = websocket.WebSocketApp(websocket_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    while True:
        try:
            # Mantém o loop rodando
            ws.run_forever()
        except Exception as e:
            print(f"Erro ao manter a conexão: {e}. Tentando reconectar em 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de tentar reconectar
            ws = websocket.WebSocketApp(websocket_url,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)

def fetch_api():
    """Função para iniciar o WebSocket em uma thread separada.""" 
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()

def enviar_mensagem_inicializacao():
    """Envia uma mensagem de inicialização ao bot.""" 
    mensagem_inicializacao = "✅ Sistema iniciado."
    try:
        send_message(mensagem_inicializacao)
        print("Mensagem de inicialização enviada com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar mensagem de inicialização: {e}")

# Chama a função para enviar a mensagem de inicialização
enviar_mensagem_inicializacao()

# Iniciar a conexão WebSocket
fetch_api()
