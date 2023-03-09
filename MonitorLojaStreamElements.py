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
from selenium import webdriver
from selenium.webdriver.common.by import By
from telesign.messaging import MessagingClient


#configuracao para envio das mensagens
#informacoes telesing
customer_id = "coloque seu customer id aqui entre aspas"
api_key = "coloque sua api key aqui entre aspas"
phone_number = "coloque seu telefone aqui entre aspas - siga o formato 5516xxxxxxxxx (cod pais + cod DDD + numero de telefone)"

paginaLoja = "https://streamelements.com/gaules/store" #link da loja aqui


#FUNCOES_______________________________________________________________________________
#envia mensagem
def send_message(mensagem,customer_id,api_key,phone_number):
    message_type = "ARN" #seleciona tipo da mensagem
    messaging = MessagingClient(customer_id, api_key) #cria cliente
    messaging.message(phone_number, mensagem, message_type) #envia mensagem


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
driver = webdriver.Chrome(executable_path='C:/Users/micao/OneDrive/dev_git/lojinhaGau/chromedriver_win32/chromedriver.exe')

#abre a pagina da loja streamelements
driver.get(paginaLoja)
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
    time.sleep(600) #espera de 10 minutos para realizar o proximo webscraping
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