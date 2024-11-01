import json
from datetime import datetime
from patterns import processar_dados  # Importa as funções processar_dados e verificar_cor

# Variáveis globais
buffer = ""
processed_ids = set()
novacor = None  # Inicializando a variável para armazenar a nova cor
novaentrada = False  # Inicializando a variável para rastrear novas entradas


def process_message(message):
    global buffer, novacor, novaentrada  # Inclua novaentrada nas variáveis globais

    buffer += message
    try:
        while buffer:
            if buffer.startswith("42"):  # Se a mensagem começar com "42"
                data = json.loads(buffer[2:])  # Carrega o conteúdo JSON ignorando os dois primeiros caracteres
                buffer = ""  # Limpa o buffer após processar a mensagem completa

                if isinstance(data, list) and len(data) > 1:
                    informacoes_relevantes = extract_relevant_info(data)
                    if informacoes_relevantes:
                        msg_id = informacoes_relevantes['id']

                        if msg_id not in processed_ids:
                            processed_ids.add(msg_id)

                            minuto = informacoes_relevantes['minute']
                            cor_resultado = informacoes_relevantes['color']
                            

                            # Atualiza a variável global novacor com a nova cor recebida
                            novacor = cor_resultado
                            novaentrada = True  # Define novaentrada como True quando nova cor é recebida

                            # Passa as informações para o processamento no patterns.py
                            processar_dados([{
                                'minute': minuto,
                                'color': cor_resultado,
                                'roll': informacoes_relevantes['roll']
                            }])  

                            # Verifica a cor após processar os dados
                            

                            print(f"ID: {msg_id}, Minuto: {minuto}, Roll: {informacoes_relevantes['roll']}, Cor: {cor_resultado}")

            else:
                buffer = ""  # Limpa o buffer se a mensagem não começar com "42"
                break
    except Exception as e:
        print(f"Erro inesperado ao processar a mensagem: {e}")

def extract_relevant_info(data):
    try:
        payload = data[1]['payload']  # Acessa o campo 'payload' na segunda posição da lista

        if payload.get("status") != "rolling":  # Verifica se o status é "rolling"
            return None

        # Extrai o horário de criação e converte para datetime
        created_at = payload.get("created_at")
        created_at_dt = datetime.fromisoformat(created_at[:-1])  # Remove o 'Z' do final para conversão correta
        minute = created_at_dt.minute

        # Monta o dicionário com as informações relevantes
        informacoes_relevantes = {
            "id": payload.get("id"),
            "color": payload.get("color"),  # Cor recebida no payload
            "roll": payload.get("roll"),
            "minute": minute,
        }
        return informacoes_relevantes
    except (KeyError, IndexError) as e:
        print(f"Erro ao extrair informações: {e}")
        return None
