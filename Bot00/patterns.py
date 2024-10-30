import time
from bot import send_message  # Importando a função de envio de mensagens

# Definições de variáveis globais
cor1 = None  # Armazena a primeira cor
cor2 = None  # Armazena a segunda cor
minuto00 = None  # Armazena a cor do minuto
sinal_enviado = False  # Indica se um sinal foi enviado
nova_cor_recebida = False  # Indica se uma nova cor foi recebida
contador_vitorias = 0  # Contador de vitórias
contador_derrotas = 0  # Contador de derrotas
minutosinal = 0  # Minuto para verificação do sinal

def processar_dados(dados):
    global cor1, cor2, minuto00, sinal_enviado, nova_cor_recebida

    nova_cor_recebida = True

    for dado in dados:
        try:
            minute = dado['minute']
            color = dado['color']

            if minute == minutosinal and not sinal_enviado:
                print("Minute é 00, processando cor.")

                if cor1 is None:
                    cor1 = color
                else:
                    cor2 = color
                    minuto00 = cor2
                    # Envio de mensagem de sinal
                    mensagem = f'''
🚨 Sinal encontrado 🚨

⏯️ Padrão: 00

💶 Entrar no {"⚫️" if minuto00 == 1 else "🔴"}

🦾 Proteger no ⚪️'''
                    send_message(mensagem)

                    sinal_enviado = True
                    nova_cor_recebida = False
                    print("Sinal enviado, aguardando nova entrada...")

        except Exception as e:
            print(f"Erro ao processar os dados: {e}")

def verificar_cor(novacor, minute):
    global sinal_enviado

    if sinal_enviado and nova_cor_recebida:
        correcao(novacor)

def correcao(novacor):
    global minuto00, sinal_enviado, contador_vitorias, contador_derrotas

    if minuto00 != novacor or novacor == 0:
        contador_vitorias += 1
        mensagem_vitoria = f"✅ WINN!"
        mensagem_contadorvitoria = f"Total de winns: {contador_vitorias}, Total de Loss: {contador_derrotas}"
        send_message(mensagem_vitoria)
        send_message(mensagem_contadorvitoria)
        
        sinal_enviado = False

    elif minuto00 == novacor:
        contador_derrotas += 1
        mensagem_derrota = f"❌ LOSS"
        mensagem_contadorderrota = f"Total de winns: {contador_vitorias}, Total de Loss: {contador_derrotas}"
        send_message(mensagem_derrota)
        send_message(mensagem_contadorderrota)
        sinal_enviado = False

def reset():
    global sinal_enviado, nova_cor_recebida

    sinal_enviado = False
    nova_cor_recebida = False
    print("REINICIADO.")
