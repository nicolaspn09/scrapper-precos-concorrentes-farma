import os
import sys
import time
import psutil
import locale
import smtplib
import psycopg2
import subprocess
import tempfile
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Tratamento de erros
def handle_exception(bloco_codigo, e):
    """
    Lida com exceções e envia e-mails de erro

    Parameters:
    bloco_codigo: string
    e: string
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    data_hora_atual = datetime.now()
    mensagem = f"Erro no acesso do site da Droga Raia. Função: {bloco_codigo}. Erro: {e}"

    destinatarios_email = ['Nicolas.nasario@COMPANY_NAME.com.br', 'Lucas.remor@COMPANY_NAME.com.br']
    assunto_email = "Erro no RPA da Droga Raia 2000-4000"
    envia_email(mensagem, destinatarios_email, assunto_email)


# Envia o e-mail de execução
def envia_email_execucao():
    #Bloco de logs
    locale.setlocale(locale.LC_ALL, 'pt_BR') #Seta o local
    data_hora_atual = datetime.now() #Busca a data atual

    # Configurações do servidor SMTP
    smtp_server = 'mail.COMPANY_NAME.com.br'
    smtp_port = 25  # Porta para comunicação segura com TLS

    # Credenciais do remetente
    remetente_email = "rpa@COMPANY_NAME.com.br"
    remetente_senha = 'REMOVED_FOR_GITHUB'

    destinatarios = ['nicolas.nasario@COMPANY_NAME.com.br', 'lucas.remor@COMPANY_NAME.com.br']

    # Crie uma mensagem MIMEMultipart
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente_email
    mensagem['To'] = ', '.join(destinatarios)
    mensagem['Subject'] = 'Python Consulta Droga Raia 4701-0'

    # Adicione o corpo do e-mail
    corpo_email = 'Olá, o Python está rodando.'
    mensagem.attach(MIMEText(corpo_email, 'plain'))  # 'plain' para texto simples ou 'html' para HTML

    try:
        servidor_smtp = smtplib.SMTP(smtp_server, smtp_port)
        servidor_smtp.starttls()  # Ative a criptografia TLS

        # Faça login com suas credenciais
        servidor_smtp.login(remetente_email, remetente_senha)

        # Envie o e-mail
        texto_email = mensagem.as_string()
        servidor_smtp.sendmail(remetente_email, destinatarios, texto_email)

    except Exception as e:
        #Bloco de logs
        locale.setlocale(locale.LC_ALL, 'pt_BR') #Seta o local
        data_hora_atual = datetime.now() #Busca a data atual
        mensagem = f"Erro ao enviar e-mail: {str(e)}" #Informa a mensagem do Log

        #Envio dos e-mails de erro
        destinatarios_email = []
        destinatarios_email.append('Nicolas.nasario@COMPANY_NAME.com.br')
        destinatarios_email.append('Lucas.remor@COMPANY_NAME.com.br')

        assunto_email = "Erro no RPA da Consulta Droga Raia 2000-4000"

        envia_email(mensagemEmail=mensagem, destinatarios_email=destinatarios_email, assunto_email=assunto_email)

    finally:
        servidor_smtp.quit()


# Envia e-mails
def envia_email(mensagemEmail, destinatarios_email, assunto_email):
    """
    Envia e-mails personalizados

    Parameters:
    MensagemEmail = string
    Destinatarios_email = collection
    Assunto_email = string
    """

    smtp_server = 'mail.COMPANY_NAME.com.br'
    smtp_port = 25
    remetente_email = "rpa@COMPANY_NAME.com.br"
    remetente_senha = 'REMOVED_FOR_GITHUB'

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente_email
    mensagem['To'] = ",".join(destinatarios_email)
    mensagem['Subject'] = assunto_email

    mensagem.attach(MIMEText(mensagemEmail, 'html'))

    #try:
    servidor_smtp = smtplib.SMTP(smtp_server, smtp_port)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente_email, remetente_senha)
    texto_email = mensagem.as_string()
    servidor_smtp.sendmail(remetente_email, destinatarios_email, texto_email)

    #except Exception as e:
        #print(e)
        #handle_exception(bloco_codigo="Envia_email", e=e)

    #finally:
    servidor_smtp.quit()


# Roda query para executar o MySQL
def conecta_pg(database, sql):
    """
    Roda query para executar o MySQL

    Parameters:
    Sql = string

    Returns:
    tabela_sql = datatable
    """

    host = 'REMOVED'  # Endereço do servidor MySQL
    database = database  # Nome do banco de dados
    user = 'REMOVED'  # Nome de usuário para acessar o banco de dados
    password = 'REMOVED_FOR_GITHUB'  # Senha do usuário para acessar o banco de dados
    port = 5432

    # Estabelece a conexão com o banco de dados
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    tabela_sql = cursor.fetchall()
    cursor.close()
    connection.close()

    # Retorna o resultado da consulta do SQL para o usuário
    return tabela_sql


# Roda query para executar o MySQL
def conecta_pg_insert(sql):
    """
    Roda query para executar o MySQL

    Parameters: 
    sql = string
    """

    host = 'REMOVED'  # Endereço do servidor MySQL
    database = 'REMOVED'  # Nome do banco de dados
    user = 'REMOVED'  # Nome de usuário para acessar o banco de dados
    password = 'REMOVED_FOR_GITHUB'  # Senha do usuário para acessar o banco de dados
    port = 5432

    # Estabelece a conexão com o banco de dados
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


# Função para encontrar subprocessos do ChromeDriver
def find_chrome_processes(ppid):
    """
    Função para encontrar subprocessos do ChromeDriver

    Parameters:
    ppid: string

    Returns:
    chrome_pids: list
    """

    chrome_pids = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name']):
        try:
            # Ajusta o nome do processo conforme necessário
            if proc.info['ppid'] == ppid and proc.info['name'].lower() in ['chrome', 'chrome.exe']:
                chrome_pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return chrome_pids


# Função para matar o Firefox
def kill_firefox():
    """
    Função para matar o Firefox
    """

    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)

    except Exception as e:
        print(e)


# Função para matar processos pelo PID
def kill_process(pid):
    """
    Função para matar processos pelo PID

    Parameters:
    pid = string
    """

    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
        else:  # Unix-based systems (Linux, Mac)
            os.kill(pid, 9)
        #print(f"Processo {pid} foi finalizado.")
    except Exception as e:
        pass
        #print(f"Erro ao tentar finalizar o processo {pid}: {e}")


# Acessa o navegador
def acessa_navegador():
    """
    Acessa o navegador
    """

    try:    
        # Configurações para o Chrome
        options = ChromeOptions()

        sys.stdout = open(r"C:\rpa\Python\Web Scrapping Droga Raia\Log.txt", 'w') #AJUSTAR
        user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        # options.add_argument('--headless')  # Executa o Chrome em modo headless (sem interface gráfica)
        options.add_argument("--window-size=1920,1080")  # Define o tamanho da janela
        options.add_argument("--disable-gpu")
        options.add_argument(user_agent)  # Define o user-agent para o Chrome
        options.add_argument('--ignore-certificate-errors')  # Desabilita a verificação de certificado SSL
        options.add_argument('--log-level=3')  # Minimiza os logs de saída
        options.add_argument('--silent')  # Modo silencioso para suprimir mensagens adicionais

        # Define o serviço do ChromeDriver
        servico = ChromeService()
        servico.log_output = open("NUL", "w")  # Redireciona a saída de log para "NUL" (não exibe)

        # Inicia o navegador Chrome com as opções definidas
        navegador = webdriver.Chrome(options=options, service=servico)

        # Maximiza o navegador
        navegador.maximize_window()  # Maximiza a tela

        # Obtém o PID do processo do ChromeDriver
        chromedriver_pid = servico.process.pid

        # Encontra subprocessos do ChromeDriver
        chrome_pids = find_chrome_processes(chromedriver_pid)

        return navegador, chrome_pids, servico

    except Exception as e:
        #print(e)
        handle_exception(bloco_codigo="Acessa_navegador", e=e)

        for pid in chrome_pids:
            kill_process(pid)


# Aceita os cookies
def aceita_cookie(navegador):
    """
    Aceita os cookies
    """

    # Aceitar Cookies
    WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

    # Verifica se o elemento está carregado na página
    elemento_cookie = navegador.find_element(By.ID, "onetrust-accept-btn-handler")

    # Espera um tempo
    time.sleep(0.5)

    # Clica nos dados cadastrais por Javascript
    navegador.execute_script("arguments[0].click();", elemento_cookie)


# Obtém as informações do produto
def obtem_informacoes_produto(navegador):
    """
    Obtém as informações do produto

    Parameters:
    navegador: navigator

    returns:
    valor_original: float
    desconto: float
    preco_final: float
    programa_desconto_laboratorio: string
    """

    valor_original_texto = ""
    valor_original = 0
    desconto_texto = ""
    desconto = 0
    preco_final_texto = ""
    preco_final = 0
    preco_multiplo_texto = ""
    preco_multiplo = 0
    tipo_desconto = ""
    loja_entrega = ""
    adicional_entrega = ""
    programa_desconto_laboratorio = "NÃO"

    try:
        # Espera aparecer o valor original
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[1]/p/span")))

        # Obtém o nome do item
        loja_entrega = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[1]/p/span").text

        if "raia" not in str(loja_entrega).lower():
            try:
                # Espera aparecer o valor original
                WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div[1]/p[1]/button")))

                # Obtém o nome do item
                adicional_entrega = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div[1]/p[1]/button").text

                # Concatena o nome da loja com o local
                loja_entrega = loja_entrega + " " + adicional_entrega

            except:
                pass

    except:
        try:
            # Espera aparecer o valor original
            WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div/p/span")))

            # Obtém o nome do item
            loja_entrega = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div/p/span").text

            if "raia" not in str(loja_entrega).lower():
                try:
                    # Espera aparecer o valor original
                    WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div[1]/p[1]/button")))

                    # Obtém o nome do item
                    adicional_entrega = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div[1]/p[1]/button").text

                    # Concatena o nome da loja com o local
                    loja_entrega = loja_entrega + " " + adicional_entrega

                except:
                    pass

        except:
            pass

    try:
        # Espera aparecer o valor original
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[1]/span")))

        # Obtém o nome do item
        valor_original_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[1]/span").text

        # Espera aparecer o desconto
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[2]/span[2]/span/span")))

        # Obtém o nome do item
        desconto_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[2]/span[2]/span/span").text

        # Espera aparecer o desconto
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[2]/span[1]")))

        # Obtém o nome do item
        preco_final_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[2]/span[1]").text

        # Espera aparecer o desconto
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[2]/div[2]/span[1]")))

        # Obtém o nome do item
        desconto_labotorio = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[5]/div[1]/p").text

        # Ajusta os dadosW
        valor_original = str(valor_original_texto).replace("R$", "").replace(",", ".").replace("%", "").strip()
        desconto = str(desconto_texto).replace("R$", "").replace("-", "").replace(",", ".").replace("%", "").strip()
        preco_final = str(preco_final_texto).replace("R$", "").replace(",", ".").replace("%", "").strip()

        if "DESCONTO" in str(desconto_labotorio).upper():
            programa_desconto_laboratorio = "SIM"

    except:
        try:
            # Espera aparecer o desconto
            WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[1]/span")))

            # Obtém o nome do item
            tipo_desconto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[1]/span").text

        except:
            pass

        for i in range(1, 4):
            try:
                # Espera aparecer o desconto
                WebDriverWait(navegador, 1).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[{i}]/div[1]/div[2]/span[1]")))

                # Obtém o nome do item
                valor_original_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[{i}]/div[1]/div[2]/span[1]").text

                valor_original = str(valor_original_texto).replace("R$", "").replace(",", ".").replace("%", "").strip()

            except:
                pass

            try:
                # Espera aparecer o desconto
                WebDriverWait(navegador, 1).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[{i}]/div[1]/div[2]/span[2]")))

                # Obtém o nome do item
                preco_final_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[{i}]/div[1]/div[2]/span[2]").text

                preco_final = str(preco_final_texto).replace("R$", "").replace(",", ".").replace("%", "").strip()

                break     

            except:
                pass

    try:
        # Espera aparecer o valor original
        WebDriverWait(navegador, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/span[2]")))

        # Obtém o nome do item
        preco_multiplo_texto = navegador.find_element("xpath", f"/html/body/div[1]/main/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/span[2]").text

        preco_multiplo = str(preco_multiplo_texto).replace("R$", "").replace(",", ".").replace("%", "").strip() 

    except:
        pass

    if float(str(preco_final).replace(".", "").replace(",", ".")) < float(str(valor_original).replace(".", "").replace(",", ".")):
        desconto = ((float(valor_original) - float(preco_final)) / float(valor_original)) * 100
        desconto = "{:.2f}".format(desconto)

    if tipo_desconto == "":
        tipo_desconto = "NORMAL"

    return valor_original, desconto, preco_final, programa_desconto_laboratorio, tipo_desconto, loja_entrega, preco_multiplo


# Acessa o site da Droga Raia
def acessa_site():
    """
    Acessa o site da Droga Raia
    """
    try:
        # Forma o SQL
        sql = f"select cd_ean from msv.dim_mercadoria where cd_ean <> 0 and cd_ean <> 9999999999999 offset 4701"

        # Consulta os EANs
        eans = conecta_pg(database = 'REMOVED', sql=sql)

        # Itera sobre os EANs
        for ean in eans:
            ean = ean[0]
            sucesso = False

            #Verifica o horário atual
            locale.setlocale(locale.LC_ALL, 'pt_BR') #Seta o local
            current_time = datetime.now().time() #Obtém a data atual

            data_convertida = current_time.strftime('%H:%M') #Converte para HH:MM

            if '04:00' in data_convertida:
                envia_email_execucao() #Envia o e-mail de que está sendo executado
            elif '08:30' in data_convertida:
                envia_email_execucao() #Envia o e-mail de que está sendo executado
            elif '13:30' in data_convertida:
                envia_email_execucao() #Envia o e-mail de que está sendo executado
            elif '17:30' in data_convertida:
                envia_email_execucao() #Envia o e-mail de que está sendo executado
            elif '21:00' in data_convertida:
                envia_email_execucao() #Envia o e-mail de que está sendo executado

            while not sucesso:
                navegador, chrome_pids, servico = acessa_navegador()

                # # Define a URL
                # url = f"https://www.drogaraia.com.br/"

                # # Acessa o site
                # navegador.get(url)

                # Ajusta a URL de busca
                url = f"https://www.drogaraia.com.br/search?w={ean}"

                # Acessa o site
                navegador.get(url)

                # Espera aparecer a tela dos cookies 
                # aceita_cookie(navegador=navegador)

                try:
                    # Verifica se retornou o produto
                    WebDriverWait(navegador, 9.5).until(EC.presence_of_element_located((By.XPATH , "/html/body/div[1]/main/main/div/div/section/section/div[2]/div[2]/article/div[3]/h2/a")))

                    # Aguarda um tempo
                    time.sleep(0.5)

                    # Obtém o nome do item
                    nome_produto = navegador.find_element("xpath", f"/html/body/div[1]/main/main/div/div/section/section/div[2]/div[2]/article/div[3]/h2/a").text

                    # Espera o nome do produto
                    elemento_produto = navegador.find_element(By.XPATH, "/html/body/div[1]/main/main/div/div/section/section/div[2]/div[2]/article/div[3]/h2/a")

                    # Espera um tempo
                    time.sleep(0.5)

                    # Clica no nome do produto
                    navegador.execute_script("arguments[0].click();", elemento_produto)

                    # Espera aparecer as informações do produto
                    valor_original, desconto, preco_final, programa_desconto_laboratorio, tipo_desconto, loja_entrega, preco_multiplo = obtem_informacoes_produto(navegador=navegador)

                    # Obtém a hora atual
                    data_atual = datetime.now()

                    # Monta o insert
                    sql = f"insert into comercial.infos_site_droga_raia (ean, nome_produto, valor_original, desconto, preco_final, programa_desconto_laboratorio, data_pesquisa, tipo_desconto, preco_multiplo, loja_entrega) values ({ean}, '{str(nome_produto).upper()}', {valor_original}, {desconto}, {preco_final}, '{programa_desconto_laboratorio}', '{data_atual}', '{str(tipo_desconto).upper()}', {preco_multiplo}, '{str(loja_entrega).upper()}')"

                    # Faz o insert na tabela
                    conecta_pg_insert(sql=sql)

                    if str(preco_final) != "0" and {str(nome_produto).upper()} != "" and {str(nome_produto).upper()} != None:
                        # Grava a informação de situação no Google sheet do DP
                        action = f"?ean={ean}&nome_produto={str(nome_produto).upper()}&preco_original={valor_original}&desconto={desconto}&preco_final={preco_final}&desconto_laboratorio={programa_desconto_laboratorio}&tipo_desconto={str(tipo_desconto).upper()}&preco_multiplo={preco_multiplo}&loja_entrega={str(loja_entrega).upper()}&data_pesquisa={data_atual}"
                        url = f"https://script.google.com/a/macros/COMPANY_NAME.com.br/s/AKfycbxHpzvGN9GAik3dvud7RlEcgeRs9yeIQ_1ahgc9RtD6vtlR_0g-8V720Hr7iDSsP293/exec{action}"

                        # Fazendo a requisição para a API
                        requests.get(url)

                except:
                    # Obtém a hora atual
                    data_atual = datetime.now()

                    # Monta o insert
                    sql = f"insert into comercial.infos_site_droga_raia (ean, nome_produto, valor_original, desconto, preco_final, programa_desconto_laboratorio, data_pesquisa, tipo_desconto, preco_multiplo, loja_entrega) values ({ean}, 'Não encontrado', 0, 0, 0, 'NÃO', '{data_atual}', '', 0, '')"

                    # Faz o insert na tabela
                    conecta_pg_insert(sql=sql)

                sucesso = True
                
                # Encerra o navegador e o serviço para liberar recursos
                navegador.quit()
                servico.stop()

                # Intervalo entre as execuções
                time.sleep(2)

                # navegador.quit()

                # for pid in chrome_pids:
                #     kill_process(pid)

                # time.sleep(1)

    except Exception as e:
        #print(e)
        handle_exception(bloco_codigo="acessa_site", e=e)

        navegador.quit()

        for pid in chrome_pids:
            kill_process(pid)


acessa_site()

mensagem_email = f"""
Olá!<br><br>

O RPA finalizou a busca dos valores da Droga Raia das infos de 2000-4000!
"""

assunto_email = f"RPA Busca Dados Droga Raia 2000-4000"

destinatarios_email = []
destinatarios_email.append("Nicolas.nasario@COMPANY_NAME.com.br")
destinatarios_email.append("Lucas.remor@COMPANY_NAME.com.br")
destinatarios_email.append("Israel.martins@COMPANY_NAME.com.br")

envia_email(mensagemEmail=mensagem_email, destinatarios_email=destinatarios_email, assunto_email=assunto_email)