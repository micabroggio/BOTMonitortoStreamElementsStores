# -*- coding: utf-8 -*-
"""
MONITORAMENTO DE ATIVIDADES DE LOJAS STREAMELEMENTS

Criado 06 de marco de 2023
Autor: Micael Fernando Broggio

Esse script eh um bot que monitora as atividades de lojas da plataforma StreamElements.
Ele serve para comunicar ao usuario se na loja monitorada houve atualizacao de produtos.
Esse aviso chega em forma de email ao usuario.
Eh necessario utilizar os frameworks selenium e smtplib.

Atualizacoes
- V2 - 2023/05/03 - aviso ao usuario a partir de email e nao mais por SMS.
_______________________________________________________________________________
"""

#imports
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#configuracao de pagina web e tempo de monitoramento
infos = open("config.txt", "r")
infos = infos.read()
infos = infos.split()
paginaLoja        = infos[2]
timeMonitoramento = infos[5]
usuario_email     = infos[8]
pass_email        = infos[11]

#FUNCOES_______________________________________________________________________
#cria mensagem para situacao da existencia de monitoramento anterior sem que a loja tenha atualizado
def create_message_last_monitor_exist_not_atualized(lista):
    mensagem01 = "A loja não atualizou desde o último monitoramento realizado.\n\n"
    mensagem02 = "Loja: " + paginaLoja + "\n\n"
    mensagem03 = "O novo monitoramento está sendo iniciado agora!\n\n"
    mensagem04 = "O monitoramento será realizado com passo de " + str(int(timeMonitoramento)/60) + " minutos.\n\n"
    mensagem05 = "A loja monitorada está com " + str(nprod) + " produtos.\n\n"#cria mensagem
    mensagem06 = "Produtos:\n"
    mensagem = mensagem01 + mensagem02 + mensagem03 + mensagem04 + mensagem05 + mensagem06 + lista
    return mensagem

#cria mensagem para situacao da existencia de monitoramento anterior com loja atualizada
def create_message_last_monitor_exist_atualized(lista):
    mensagem01 = "A loja ATUALIZOU!\n\n"
    mensagem02 = "Loja: " + paginaLoja + "\n\n"
    mensagem03 = "O novo monitoramento está sendo iniciado agora!\n\n"
    mensagem04 = "O monitoramento será realizado com passo de " + str(int(timeMonitoramento)/60) + " minutos.\n\n"
    mensagem05 = "A loja monitorada está com " + str(nprod) + " produtos.\n\n"#cria mensagem
    mensagem06 = "Produtos:\n"
    mensagem = mensagem01 + mensagem02 + mensagem03 + mensagem04 + mensagem05 + mensagem06 + lista
    return mensagem

#cria mensagem para situacao de nao existencia de monitoramento anterior
def create_message_first_monitoring(lista):
    mensagem01 = "O monitoramento está sendo iniciado agora!\n\n"
    mensagem02 = "Loja: " + paginaLoja + "\n\n"
    mensagem03 = "O monitoramento será realizado com passo de " + str(int(timeMonitoramento)/60) + " minutos.\n\n"
    mensagem04 = "A loja monitorada está com " + str(nprod) + " produtos.\n\n"#cria mensagem
    mensagem05 = "Produtos:\n"
    mensagem = mensagem01 + mensagem02 + mensagem03 + mensagem04 + mensagem05 + lista
    return mensagem

#cria mensagem de atualizacao para bot em execucao
def create_message_monitoring(lista):
    mensagem01 = "A loja ATUALIZOU!\n\n"
    mensagem02 = "Loja: " + paginaLoja + "\n\n"
    mensagem03 = "O monitoramento está sendo realizado com passo de " + str(int(timeMonitoramento)/60) + " minutos.\n\n"
    mensagem04 = "A loja monitorada está com " + str(nprod) + " produtos.\n\n"#cria mensagem
    mensagem05 = "Produtos:\n"
    mensagem = mensagem01 + mensagem02 + mensagem03 + mensagem04 + mensagem05 + lista
    return mensagem
   
#encontra a quantidadde e os produtos disponiveis na loja
def find_products(xpage):
    produtos = xpage.find_elements(By.CLASS_NAME, "item-title")
    nprod = len(produtos)
    return produtos, nprod

#cria lista dos produtos disponiveis
def list_create(produtos):
    listaCompleta = ""
    for i in produtos:
        produto = (i.get_attribute("title"))
        listaCompleta = listaCompleta + produto + "\n"
    return listaCompleta
    
#envia mensagem
def send_message(mensagem,assunto,smtp,cabecalho):
    #inseri assunto ao cabecalho
    cabecalho['assunto'] = assunto
    
    #criar a mensagem do e-mail
    msg = MIMEMultipart('alternative')
    msg['From'] = cabecalho['de']
    msg['To'] = ', '.join(cabecalho['para'])
    msg['Subject'] = cabecalho['assunto']
    
    texto = MIMEText(mensagem, 'plain')
    msg.attach(texto)
    
    #envia o e-mail
    with smtplib.SMTP(smtp['server'], smtp['port']) as server:
        server.starttls()
        server.login(smtp['user'], smtp['password'])
        server.sendmail(cabecalho['de'], cabecalho['para'], msg.as_string())
#______________________________________________________________________________


#CONFIGURACAO EMAIL____________________________________________________________
#configura os parâmetros do servidor SMTP
smtp = {'server':'smtp.gmail.com',
        'port':587,
        'user':usuario_email,
        'password':pass_email}

#configurar o cabeçalho do e-mail
cabecalho = {'de':smtp['user'],
             'para':['micaoceano@gmail.com']}
#______________________________________________________________________________


#inicia navegador chromedriver executado a partir de path selecionado
driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

#abre a pagina da loja streamelements
driver.get(paginaLoja)
time.sleep(5)

#encontra os produtos disponiveis na loja
produtos, nprod = find_products(driver)

#cria lista dos produtos disponiveis
lista_completa = list_create(produtos)   

#tratamento de erros - 
try:
    #abre o arquivo de ultimo monitoramento caso existir
    arquivo = open("last_monitor.txt", "r")
    last_monitor = arquivo.read()
    arquivo.close()
    
    #comparativo de monitoramento - armazenado vs atual
    #armazenado = atual
    if last_monitor == lista_completa:
        
        # cria e envia mensagem
        mensagem = create_message_last_monitor_exist_not_atualized(lista_completa)
        assunto = "A loja StreamElements NÃO ATUALIZOU desde o último monitoramento."
        send_message(mensagem,assunto,smtp,cabecalho)
    
    #armazenado diferente do atual
    else:
        
        #cria e envia mensagem
        mensagem = create_message_last_monitor_exist_atualized(lista_completa)
        assunto = "A loja StreamElements ATUALIZOU!!!"
        send_message(mensagem,assunto,smtp,cabecalho)
        
        #cria arquivo de armazenamento do ultimo monitoramento
        with open("last_monitor.txt", "w") as arquivo:
            arquivo.write(lista_completa)
            arquivo.close()

#caso nao exista arquivo do ultimo monitoramento
except:
    
    #cria e envia mensagem
    mensagem = create_message_first_monitoring(lista_completa)
    assunto = "O monitoramento da loja StreamElements iniciou."
    send_message(mensagem,assunto,smtp,cabecalho)
    
    #cria arquivo de armazenamento do ultimo monitoramento
    with open("last_monitor.txt", "w") as arquivo:
        arquivo.write(lista_completa)
        arquivo.close()

#iteracao while para o monitoramento se manter constante
while 1 == 1:    
    
    #abre a pagina da loja streamelements
    time.sleep(int(timeMonitoramento))
    driver.get(paginaLoja)
    time.sleep(5)
    
    #encontra produtos disponiveis
    produtos_atual, nprod = find_products(driver)
    
    #cria lista com produtos disponiveis
    lista_completa_atual = list_create(produtos_atual)
    
    #comparativo entre listas de produtos
    #lista anterior diferente da lista atual
    if lista_completa != lista_completa_atual:  
        
        #cria e envia mensagem
        mensagem = create_message_monitoring(lista_completa)        
        assunto = "A loja StreamElements ATUALIZOU!!!"
        send_message(mensagem,assunto,smtp,cabecalho)
        
        #atualiza a lista de produtos com os novos produtos
        lista_completa = lista_completa_atual
        
        #cria arquivo de armazenamento do ultimo monitoramento
        with open("last_monitor.txt", "w") as arquivo:
            arquivo.write(lista_completa)
            arquivo.close()

        time.sleep(5)
        
    #lista anterior = lista atual 
    else:
        time.sleep(5) 