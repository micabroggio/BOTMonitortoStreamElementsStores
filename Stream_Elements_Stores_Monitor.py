# -*- coding: utf-8 -*-
"""
MONITORAMENTO DE ATIVIDADES DE LOJAS STREAMELEMENTS

Criado 06 de marco de 2023
Autor: Micael Fernando Broggio

Esse script eh um bot que monitora as atividades de lojas da plataforma StreamElements.
Ele serve para comunicar ao usuario se na loja monitorada houve atualizacao de produtos.
Esse aviso chega em forma de SMS ao aparelho celular do usuario.
Eh necessario utilizar os frameworks selenium e telesing.
    Para isso eh necessario baixar ambos e acessar https://www.telesign.com para realizar cadastro
    Solicite um customer_id e um api_key ao telesing.

ATENCAO!
LEMBRE DE PREENCHER CORRETAMENTE AS VARIAVEIS
customer_id, api_key, phone_number e paginaLoja  
"""

#imports de frameworks

import time

from telesign.messaging import MessagingClient
from selenium import webdriver
from selenium.webdriver.common.by import By

#configuracao para envio das mensagens
#informacoes telesing
infos = open("config.txt", "r")
infos = infos.read()
infos = infos.split()
customer_id = infos[2]
api_key = infos[5]
phone_number = infos[8]
paginaLoja = infos[11]
timeMonitoramento = float(infos[14])


#FUNCOES_______________________________________________________________________________
#envia mensagem
def send_message(mensagem,customer_id,api_key,phone_number):
    message_type = "ARN"
    messaging = MessagingClient(customer_id, api_key)
    messaging.message(phone_number, mensagem, message_type)


#cria lista dos produtos disponiveis
def list_create(produtos):
    listaCompleta = "Prod\n \n"
    for i in produtos:
        produto = (i.get_attribute("title"))
        listaCompleta = listaCompleta + produto + "\n"
    return listaCompleta


#encontra os produtos disponiveis na loja
def find_products(xpage):
    produtos = xpage.find_elements(By.CLASS_NAME, "item-title")
    nprod = len(produtos) #encontra o numero de produtos existentes na loja
    return produtos, nprod
#______________________________________________________________________________________


#inicia navegador chromedriver executado a partir de path selecionado
driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

#abre a pagina da loja streamelements
driver.get('https://streamelements.com/gaules/store')
time.sleep(5) #espera de 5 segundos

#encontra os produtos disponiveis na loja
produtos, nprod = find_products(driver)

#cria lista dos produtos disponiveis
listaCompleta = list_create(produtos)

#desenvolvimento e envio da primeira mensagem do monitoramento
mensagem = "A loja monitorada estah com " + str(nprod) + " produtos." #cria mensagem
send_message(mensagem,customer_id,api_key,phone_number)

#iteracao while para o monitoramento se manter constante
while 1 == 1:    
    #abre a pagina da loja streamelements
    time.sleep(timeMonitoramento) #espera de 10 minutos para realizar o proximo webscraping
    driver.get(paginaLoja) #navega a loja novamente
    time.sleep(5) #espera de 5 segundos

    produtosAtual, nprod = find_products(driver)
    
    listaCompletaAtual = list_create(produtosAtual)
    
    if listaCompleta != listaCompletaAtual:       
        mensagem = "A sua loja monitorada foi atualizada!!!\nAgora ela esta com " + str(nprod) + " produtos."
        send_message(mensagem,customer_id,api_key,phone_number)
        listaCompleta = listaCompletaAtual
        time.sleep(5) 
    else:
        time.sleep(5) 