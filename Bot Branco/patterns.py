import time
from bot import send_message  # Importando a função de envio de mensagens

# Definições de variáveis globais
sinal_enviado = False  # Indica se um sinal foi enviado
b1, b2, b3 = None, None, None  # Armazena os minutos + 6, + 10, + 12
mensagens_enviadas = set()  # Para armazenar combinações já enviadas

def processar_dados(dados):
    global sinal_enviado, b1, b2, b3

    for dado in dados:
        try:
            minute = dado['minute']
            color = dado['color']

            # Verifica se a cor é 0 e um sinal ainda não foi enviado
            if color == 0 and not sinal_enviado:
                # Armazenar os minutos prováveis
                b1 = (minute + 6) % 60
                b2 = (minute + 10) % 60
                b3 = (minute + 12) % 60

                # Criar chave única para os minutos
                mensagem_key = (b1, b2, b3)

                # Verifica se a mensagem ainda não foi enviada
                if mensagem_key not in mensagens_enviadas:
                    # Calcular e formatar os horários
                    hora_atual = time.localtime().tm_hour
                    horario_b1 = f"{(hora_atual + (minute + 6) // 60) % 24}:{(minute + 6) % 60:02d}"
                    horario_b2 = f"{(hora_atual + (minute + 10) // 60) % 24}:{(minute + 10) % 60:02d}"
                    horario_b3 = f"{(hora_atual + (minute + 12) // 60) % 24}:{(minute + 12) % 60:02d}"

                    # Enviar mensagem
                    mensagem = f'''
✅ Entrada Confirmada 🎯
⏰ Horários

⚪ {horario_b1}
⚪ {horario_b2}
⚪ {horario_b3}
'''
                    send_message(mensagem)
                    print("Mensagem enviada")

                    # Marcar como enviado
                    mensagens_enviadas.add(mensagem_key)
                    sinal_enviado = True

            # Verifica se o minuto atual é maior que b3
            if sinal_enviado and minute > b3:
                sinal_enviado = False  # Permite nova análise após o b3
                # Resetar as variáveis b1, b2 e b3
                b1, b2, b3 = None, None, None

        except Exception as e:
            print(f"Erro ao processar os dados: {e}")
