import websocket
import json
import threading
from data_handler import process_message
import time

def on_message(ws, message):
    """Callback para mensagens recebidas."""
    process_message(message)

def on_error(ws, error):
    """Callback para erros."""
    print(f"Erro: {error}")  # Log de erro

def on_close(ws, close_status_code, close_msg):
    """Callback para fechamento da conexão."""
    
    time.sleep(5)  # Espera antes de tentar reconectar
    start_websocket()  # Tenta reconectar

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

    # Mantém o loop rodando
    ws.run_forever()

def fetch_api():
    """Função para iniciar o WebSocket em uma thread separada."""
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()
