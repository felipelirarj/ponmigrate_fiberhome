import requests
from socket import *
import time
import mysql.connector
from getpass import getpass
import re
import sqlite3


print("""

zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
zz       zzz  zzzzzzzzzzzzzzzzzzzzz  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
zz  zzzzz  z  zzzzzzzzzzzzzzzzzzzzz  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
zz  zzzzzzzz  zzzzzzzzzzzzzzzzzzzzz  zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
zz      zzzz     zzzz     zz  zz  z      zzzz    zzzz   z  zzz     zzz
zz  zzzzz  z  zz  zz  zzz  z  z  zz  zzz  zz  zz  zz  z  z  z  zzz  zz
zz  zzzzz  z  zzz  z      zz   zzzz  zzz  z  zzzz  z  z  z  z      zzz
zz  zzzzz  z  zz  zz  zzzzzz  zzzzz  zzz  zz  zz  zz  z  z  z  zzzzzzz
zz  zzzzz  z     zzzz      z  zzzzz  zzz  zzz    zzz  z  z  zz      zz
zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

SISTEM OF MIGRATION ONUS | ONTS FIBERHOME WITH TL1

AUTHOR: FELIPE LIRA
DATE: 19/02/2024

""")


#Informando o endereço IPv4 do UNM2000 e realizando a verificação se o endereço é válido!
server = input("Informe o endereço IPv4 do servidor UNM2000: ")
match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{server}")

while bool(match) == False:
    print("Endereço de IPv4 inválido!")
    print("Formato aceito: xxx.xxx.xxx.xxx")
    server = input("Informe o endereço IPv4 do servidor UNM2000: ")
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{server}")



user = input("Informe o seu usuario do UNM2000: ")
while user == '':
   user = input("Informe o seu usuario do UNM2000: ")

  
password = getpass("Informe a sua senha do UNM2000: ")
while password == '':
    password = getpass("Informe a sua senha do UNM2000: ")   




#Informando os endereço de IPv4 das OLTs de Origem e Destino
    
ip_olt_origem = input("Informe o IPv4 da OLT de ORIGEM: ")
match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{ip_olt_origem}")
while bool(match) == False:
    print("Endereço de IPv4 inválido!")
    print("Formato aceito: xxx.xxx.xxx.xxx")
    ip_olt_origem = input("Informe o endereço IPv4 da OLT de Origem: ")
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{ip_olt_origem}")

ip_olt_destino = input("Informe o IPv4 da OLT de DESTINO: ")
match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{ip_olt_destino}")
while bool(match) == False:
    print("Endereço de IPv4 inválido!")
    print("Formato aceito: xxx.xxx.xxx.xxx")
    ip_olt_destino = input("Informe o endereço IPv4 da OLT de Destino: ")
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{ip_olt_destino}")    



#Fazendo Login no TL1 do UNM2000
try:
    login1 = f'LOGIN:::CTAG::UN={user},PWD={password};'
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server , 3337))
    s.send(login1.encode())
    time.sleep(1)
    
except:
    print("Erro ao realizar o login no TL1")
    exit(0)

    
print("\n\n")


#Conexao com o database do UNM2000
dataBase = mysql.connector.connect(
                     host = server,
                     user = "USUARIO_DB_UNM2000",
                     passwd = "SENHA_DB_UNM2000",
                     database = "integratecfgdb" )

cursorObject = dataBase.cursor()
   
#Pesquisando o ID da OLT de Origem
query = f"select `cobjectname`, `cobjectid` from `integratecfgdb`.`t_nedevice` where cipaddress='{ip_olt_origem}';"
cursorObject.execute(query)
myresult = cursorObject.fetchall()

#Coletando e adicionando a variaveis o nome da OLT e o ID 
for x in myresult:
    description = (x[0])
    cneid_origem =(x[1])
    print('\nOLT Origem\n')
    print(f"OLT: {description}")
    print(F"ID Da OLT: {cneid_origem}")
    print("-"*20)
    print('\n\n')


#Pesquisando o ID da OLT de Destino
query = f"select `cobjectname`, `cobjectid` from `integratecfgdb`.`t_nedevice` where cipaddress='{ip_olt_destino}';"
cursorObject.execute(query)
myresult = cursorObject.fetchall()

#Coletando e adicionando a variaveis o nome da OLT e o ID 
for x in myresult:
    description = (x[0])
    cneid_destino =(x[1])
    print('\nOLT Destino\n')
    print(f"OLT: {description}")
    print(F"ID Da OLT: {cneid_destino}")
    print("-"*20)
    print('\n\n')

#Coletando informações do SLOT e PON de Origem e Destino   
print("OLT DE ORIGEM")
slot_number_origem = input("Informe o slot: ")
pon_number_origem = input("Informe a PON: ")
print("\n\n")

print("OLT DE DESTINO")
slot_number_destino = input("Informe o slot: ")
pon_number_destino = input("Informe a PON: ")
print("\n\n")


tempo_inicial = time.time()

#################################################
#print("CONSULTANDO INFORMAÇÕES DA CELULA ORIGEM")
query1 = f"SELECT a.cobjectid as cneid_olt, b.cobjectid as cslot_id_olt, c.cidentifier as cell_name from integratecfgdb.t_nedevice a, integratecfgdb.t_boarddevice b ,  integratecfgdb.t_objectidentifier c WHERE a.cipaddress='{ip_olt_origem}' AND b.cparentid = a.cobjectid AND c.cportno='{pon_number_origem}' AND b.cobjectno='{slot_number_origem}' and c.cobjectid=b.cobjectid;"
cursorObject.execute(query1)
 
myresult = cursorObject.fetchall()
myresult = str(myresult).strip('[]')
myresult = myresult.split(',')
cell_name = myresult[2]
cell_name = cell_name.strip()
cell_name = cell_name.split('(')
cell_name = cell_name[1]
cell_name = cell_name.split(' ')
cell_name = cell_name[1]
vlan_id_pon_origem = cell_name.replace(')','').replace("'",'')

print(f'VLAN OLT ORIGEM: {vlan_id_pon_origem}')


#print("CONSULTANDO INFORMAÇÕES DA CELULA DESTINO")
query1 = f"SELECT a.cobjectid as cneid_olt, b.cobjectid as cslot_id_olt, c.cidentifier as cell_name from integratecfgdb.t_nedevice a, integratecfgdb.t_boarddevice b ,  integratecfgdb.t_objectidentifier c WHERE a.cipaddress='{ip_olt_destino}' AND b.cparentid = a.cobjectid AND c.cportno='{pon_number_destino}' AND b.cobjectno='{slot_number_destino}' and c.cobjectid=b.cobjectid;"
cursorObject.execute(query1)
 
myresult = cursorObject.fetchall()
myresult = str(myresult).strip('[]')
myresult = myresult.split(',')
cell_name = myresult[2]
cell_name = cell_name.strip()
cell_name = cell_name.split('(')
cell_name = cell_name[1]
cell_name = cell_name.split(' ')
cell_name = cell_name[1]
vlan_id_pon_destino = cell_name.replace(')','').replace("'",'')

print(f'VLAN OLT DESTINO: {vlan_id_pon_destino}')



#Buscando todas as ONUs do SLOT e PON da OLT de Origem
query = f"SELECT `cslotno`,  `cponno`,`cauthno`, `contmac`, `cobjectname`, `cequipmentid` FROM `integratecfgdb`.`t_ontdevice` where cneid='{cneid_origem}' and cslotno='{slot_number_origem}' and cponno='{pon_number_origem}';"
cursorObject.execute(query)
myresult = cursorObject.fetchall()

#Informando o numero de registros a serem analisados
total_onus = len(myresult)
print(f"Total de ONUs a serem analisadas: {total_onus}\n\n")


#Para cada linha de ONU, o envio dos comandos para verificar informações do equipamento ONU 
numero_linhas = 0 
for x in myresult:
    auth = x[2]
    serial_onu1 = x[3]
    nome_cliente1 = x[4]
    numero_linhas += 1
    modelo_onu = x[5]
    
    print(f"Verificando as informações da ONU: {serial_onu1} \nCliente: {nome_cliente1}")
    print(f"Modelo da ONU: {modelo_onu}")


    try:    
        s.send(f'LST-OMDDM::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
        time.sleep(0.5) 
        rcv = s.recv(4096)

        retorno = rcv.decode()
        retorno = retorno.split()
        localiza = retorno.index('PRxPower')
        localiza = localiza + 2
        final = localiza + 1

        temperatura = localiza + 6
        temp_final = localiza + 7
    
        sinal = retorno[localiza:final]
        temperatura = retorno[temperatura:temp_final]
        temperatura = str(temperatura)
        sinal = str(sinal)
        sinal = sinal.replace("'",'').replace('[','').replace(']','').replace(',','.')
        temperatura = temperatura.replace("'",'').replace('[','').replace(']','').replace(',','.')

    except ValueError:
        print("Erro ao consultar o sinal... Tentando novamente")
        try:
            s.send(f'LST-OMDDM::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
            time.sleep(0.5) 
            rcv = s.recv(4096)

            retorno = rcv.decode()
            retorno = retorno.split()
            localiza = retorno.index('PRxPower')
            localiza = localiza + 2
            final = localiza + 1

            temperatura = localiza + 6
            temp_final = localiza + 7
    
            sinal = retorno[localiza:final]
            temperatura = retorno[temperatura:temp_final]
            temperatura = str(temperatura)
            sinal = str(sinal)
            sinal = sinal.replace("'",'').replace('[','').replace(']','').replace(',','.')
            temperatura = temperatura.replace("'",'').replace('[','').replace(']','').replace(',','.')

        except ValueError:
            print("Erro ao consultar o sinal.. Encerrando a aplicacao")
        
            exit(0)
    
    #verificar versao de firmware da onu
    s.send(f'LST-ONUVERSION::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
    time.sleep(0.5)
    rcv = s.recv(4096)

    #Se for WKE2.134.321F1G, o modelo será AN5506-02-F
    if 'WKE2.134.321F1G' in rcv.decode():
        modelo_onu = 'AN5506-02-F'

    elif 'BR_1.03-200723' in rcv.decode():
        modelo_onu = 'AN5506-01-A1'

    elif 'PDTC' in serial_onu1:
        print("------------------------------ Padtec ONU ------------------------------")
        modelo_onu = 'AN5506-01-A1'

    elif 'WKE2.134.285B5' in rcv.decode():
        modelo_onu = 'AN5506-04-B2'
    elif 'WKE2.134.321B7G' in rcv.decode():
        modelo_onu = 'AN5506-02-B'
        
    else:
        pass
    
    #Verifica o sinal óptico da ONU. Se o sinal for 0, a ONU não será consultada. Isso impede o provisionamento de ONUs offline ;)
    if sinal == '0.00':
        print("ONU SEM SINAL")
    
    else:
            
        try:
            s.send(f'ADD-ONU::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino}:CTAG::AUTHTYPE=MAC,ONUID={serial_onu1},ONUTYPE={modelo_onu},NAME={nome_cliente1};'.encode())
            time.sleep(1) 
            rcv = s.recv(4096)
            retorno = rcv.decode()
            if 'DENY' in retorno:
                print(f"Erro ao Autorizar a ONU: {serial_onu1}")
            else:
                print(f"Sucesso ao Autorizar a ONU: {serial_onu1}")
        except:
            pass
        
        if modelo_onu == 'AN5506-01-A1' or modelo_onu == 'HG260' or modelo_onu  == 'AN5506-02-B' or modelo_onu == '0000000000000000000' or modelo_onu == 'RTL9602C' or modelo_onu == 'AN5506-04-B2':
            print(f'Sinal ONU: {sinal}')
            print(f'Temperatura ONU: {temperatura}ºC')

            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-1')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan1 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 1: {vlan1}')
                vlan_lan1 = vlan1

                if 'CORP - ' in nome_cliente1:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_lan1},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")

                else:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                    
            except:
                vlan_lan1 = ''
                pass
            
            
           

        elif modelo_onu == 'AN5506-04-FA' or modelo_onu == 'HG6143D' or modelo_onu == 'HG6245D' or modelo_onu == 'HG6143D3' or modelo_onu == 'HG6145F':

            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-1')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan1 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 1: {vlan1}')
                vlan_lan1 = vlan1

                if 'CORP - ' in nome_cliente1:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_lan1},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")

                else:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")

                    
            except:
                vlan_lan1 = ''
                pass

            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-2:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-2')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan2 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 2: {vlan2}')
                vlan_lan2 = vlan2
                
                if 'CORP - ' in nome_cliente1:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-2:CTAG::CVLAN={vlan_lan2},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")

                else:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-2:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")


                    
            except:
                vlan_lan2 = ''
                pass
            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-3:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-3')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan3 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 3: {vlan3}')
                vlan_lan3 = vlan3
                
                if 'CORP - ' in nome_cliente1:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-3:CTAG::CVLAN={vlan_lan3},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")

                else:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-3:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")


                    
            except:
                vlan_lan3 = ''
                pass

            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-4:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-4')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan4 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 4: {vlan4}')
                vlan_lan4 = vlan4

                
                if 'CORP - ' in nome_cliente1:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-4:CTAG::CVLAN={vlan_lan4},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")

                else:
                    s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-4:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                    time.sleep(1) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if 'DENY' in retorno:
                        print(f"Erro ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")
                    else:
                        print(f"Sucesso ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")

                    
            except:
                vlan_lan4 = ''
                pass
 
            
            if vlan_lan1 == '' and vlan_lan2 == '' and vlan_lan3 == '' and vlan_lan4 == '':
                
                print("Verificando WAN Service")
                try:
                    s.send(f'LST-ONUWANSERVICECFG::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                    time.sleep(0.5) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    
                    if  'DENY' in retorno:
                       pass
                    else:
                        if 'route' in retorno:    
                            print("ONU em Router")
                            localizar = retorno.split()
                            
                            vlan_pppoe = localizar.index("INTERNET")
                            vlan_pppoe = vlan_pppoe + 2
                            vlan_final = vlan_pppoe + 1
                            vlan = localizar[vlan_pppoe:vlan_final]
                            vlan = str(vlan)
                            vlan = vlan.replace("'",'').replace('[','').replace(']','')
                            modo = localizar[vlan_final:]
                            modo_conexao = vlan_final + 2
                            modo_conexao_fim = modo_conexao + 1
                            login_pppoe_inicio = modo_conexao + 15
                            login_pppoe_fim = login_pppoe_inicio + 1
                            login_pppoe = localizar[login_pppoe_inicio:login_pppoe_fim]
                            login_pppoe = str(login_pppoe)
                            login_pppoe = login_pppoe.replace("'",'').replace('[','').replace(']','')
                            senha_pppoe_inicio = login_pppoe_fim
                            senha_pppoe_fim = senha_pppoe_inicio + 1
                            senha_pppoe = localizar[senha_pppoe_inicio:senha_pppoe_fim]
                            senha_pppoe = str(senha_pppoe)
                            senha_pppoe = senha_pppoe.replace("'",'').replace('[','').replace(']','')                        
                            modo_conexao = localizar[modo_conexao:modo_conexao_fim]
                            modo_conexao = str(modo_conexao)
                            modo_conexao = modo_conexao.replace("'",'').replace('[','').replace(']','')
                            bind_of_ports = localizar.index("33024")
                            bind_inicio = bind_of_ports + 5
                            bind_final = bind_inicio + 1
                            portas_bind = localizar[bind_inicio:bind_final]
                            portas_bind = str(portas_bind)
                            portas_bind = portas_bind.replace("-",' ')
                            portas_bind = portas_bind.replace("'",'').replace('[','').replace(']','')
                            
                            print(f'VLAN PPPoE: {vlan}')
                            print(f'Modo de conexão: {modo_conexao}')
                            print(f'Login PPPoE: {login_pppoe}')
                            print(f'Senha PPPoE: {senha_pppoe}')
                            print(f'Porta bindadas: {portas_bind}')

                            #Configurar WAN Service
                                
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,UPORT=0;'.encode())
                                time.sleep(1)
                                
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                            except:
                                pass

                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,SSID=1;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                            except:
                                pass

                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,SSID=5;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service WLAN 5.8GHZ na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service WLAN 5.8GHZ na ONU: {serial_onu1}")
                            except:
                                pass
                            
                            print("\nVerificando WIFI Service")
                            
                            try:
                                s.send(f'LST-WIFISERVICE::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
                                time.sleep(0.5) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if  'DENY' in retorno:
                                   pass
                                else:
                                    retorno = retorno.split()
                                    ssid5g = retorno[152]
                                    senha5g = retorno[157]

                                    senha_24ghz = retorno[53]
                                    ssid_24ghz = retorno[48]
                                    
                                    print(f'SSID 2.4Ghz: {ssid_24ghz}')
                                    print(f'Senha 2.4Ghz: {senha_24ghz}')
                                    print(f'SSID 5.8Ghz: {ssid5g}')
                                    print(f'Senha 5.84Ghz: {senha5g}')



                                    try:
                                        s.send(f'MODIFY-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::WORKING-FREQUENCY=2.4Ghz,FREQUENCY-BANDWIDTH=20/40MHZ,ENABLE=enable,SSID-ENABLE=1,SSID-NAME={ssid_24ghz},PRESHARED-KEY={senha_24ghz},SSID=1,WILESS-STANDARD=802.11bgn,AUTH-MODE=WPAPSK/WPA2PSK,ENCRYP-TYPE=TKIPAES;'.encode())
                                        time.sleep(1)
                                        s.send(f'MODIFY-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::WORKING-FREQUENCY=5.8Ghz,FREQUENCY-BANDWIDTH=80MHZ,ENABLE=enable,SSID-ENABLE=1,SSID-NAME={ssid5g},PRESHARED-KEY={senha5g},SSID=1,WILESS-STANDARD=802.11ac,AUTH-MODE=WPAPSK/WPA2PSK,ENCRYP-TYPE=TKIPAES;'.encode())
                                        time.sleep(1) 
                                        rcv = s.recv(4096)
                                        retorno = rcv.decode()
                                        
                                        if 'DENY' in retorno:
                                            print(f"Erro ao Autorizar a ONU: {serial_onu1}")
                                        else:
                                            print(f"Sucesso ao Autorizar a ONU: {serial_onu1}")
                                    except:
                                        pass
 
                            except:
                               pass
                                
                        else:
                            print("ONU Em bridge")
                except:
                   pass

                
                

                
        elif modelo_onu == 'AN5506-04-F1':

            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-1')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan1 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 1: {vlan1}')
                vlan_lan1 = vlan1
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_lan1},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
            except:
                vlan_lan1 = ''
                pass

            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number}-{pon_number},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-2:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-2')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan2 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 2: {vlan2}')
                vlan_lan2 = vlan2
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-2:CTAG::CVLAN={vlan_lan2},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
            except:
                vlan_lan2 = ''
                pass
            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-3:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-3')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan3 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 3: {vlan3}')
                vlan_lan3 = vlan3
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-3:CTAG::CVLAN={vlan_lan3},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 3 em Bridge ONU: {serial_onu1}")
            except:
                vlan_lan3 = ''
                pass

            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-4:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-4')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan4 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 4: {vlan4}')
                vlan_lan4 = vlan4
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-4:CTAG::CVLAN={vlan_lan4},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 4 em Bridge ONU: {serial_onu1}")
            except:
                vlan_lan4 = ''
                pass
 
            
            if vlan_lan1 == '' and vlan_lan2 == '' and vlan_lan3 == '' and vlan_lan4 == '':
                #print("Não possui config da PORT Service")
                
                print("Verificando WAN Service")
                try:
                    s.send(f'LST-ONUWANSERVICECFG::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                    time.sleep(0.5) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if  'DENY' in retorno:
                       pass
                    else:
                        if 'route' in retorno:    
                            print("ONU em Router")
                            localizar = retorno.split()  
                            vlan_pppoe = localizar.index("INTERNET")
                            vlan_pppoe = vlan_pppoe + 2
                            vlan_final = vlan_pppoe + 1
                            vlan = localizar[vlan_pppoe:vlan_final]
                            vlan = str(vlan)
                            vlan = vlan.replace("'",'').replace('[','').replace(']','')
                            modo = localizar[vlan_final:]
                            modo_conexao = vlan_final + 2
                            modo_conexao_fim = modo_conexao + 1
                            login_pppoe_inicio = modo_conexao + 15
                            login_pppoe_fim = login_pppoe_inicio + 1
                            login_pppoe = localizar[login_pppoe_inicio:login_pppoe_fim]
                            login_pppoe = str(login_pppoe)
                            login_pppoe = login_pppoe.replace("'",'').replace('[','').replace(']','')

                            senha_pppoe_inicio = login_pppoe_fim
                            senha_pppoe_fim = senha_pppoe_inicio + 1
                            senha_pppoe = localizar[senha_pppoe_inicio:senha_pppoe_fim]

                            senha_pppoe = str(senha_pppoe)
                            senha_pppoe = senha_pppoe.replace("'",'').replace('[','').replace(']','')
                                                        
                            
                            modo_conexao = localizar[modo_conexao:modo_conexao_fim]

                            modo_conexao = str(modo_conexao)
                            modo_conexao = modo_conexao.replace("'",'').replace('[','').replace(']','')

                            bind_of_ports = localizar.index("33024")

                            bind_inicio = bind_of_ports + 5
                            bind_final = bind_inicio + 1

                            portas_bind = localizar[bind_inicio:bind_final]
                            portas_bind = str(portas_bind)
                            portas_bind = portas_bind.replace("-",' ')
                            portas_bind = portas_bind.replace("'",'').replace('[','').replace(']','')
                            
                            print(f'VLAN PPPoE: {vlan}')
                            print(f'Modo de conexão: {modo_conexao}')
                            print(f'Login PPPoE: {login_pppoe}')
                            print(f'Senha PPPoE: {senha_pppoe}')
                            print(f'Porta bindadas: {portas_bind}')

                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,UPORT=0;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                            except:
                                pass

                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,SSID=1;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                            except:
                                pass


                            print("\nVerificando WIFI Service")

                            try:
                                s.send(f'LST-WIFISERVICE::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
                                time.sleep(0.5) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if  'DENY' in retorno:
                                   pass
                                else:

                                    retorno = retorno.split()

                                    senha_24ghz = retorno[53]
                                    ssid_24ghz = retorno[48]
                                    
                                    print(f'SSID 2.4Ghz: {ssid_24ghz}')
                                    print(f'Senha 2.4Ghz: {senha_24ghz}')
                                    
                                    #Configurar WIFI
                                    try:
                                        s.send(f'CFG-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}::ENABLE=enable,WILESSAREA=5,WILESSCHANNEL=0,WILESSSTANDARD=802.11bgn,WORKINGFREQUENCY=2.4GHZ,T-POWER=140,SSID=1,SSIDENABLE=0,SSIDNAME={ssid_24ghz},SSIDVISIBALE=1,AUTHMODE=WPAPSK,ENCRYPTYPE=TKIP,PRESHAREDKEY={senha_24ghz},UPDATEKEYINTERVAL=3600,FREQUENCYBANDWIDTH=20/40MHZ;'.encode())
                                        time.sleep(1) 
                                        rcv = s.recv(4096)
                                        retorno = rcv.decode()
                                        
                                        if 'DENY' in retorno:
                                            print(f"Erro ao Configurar a ONU: {serial_onu1}")
                                        else:
                                            print(f"Sucesso ao Configurar a ONU: {serial_onu1}")                                    
                                    except:
                                        pass
                                    
                                    try:
                                        s.send(f'MODIFY-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::WORKING-FREQUENCY=2.4Ghz,FREQUENCY-BANDWIDTH=20/40MHZ,ENABLE=enable,SSID-ENABLE=1,SSID-NAME={ssid_24ghz},PRESHARED-KEY={senha_24ghz},SSID=1,WILESS-STANDARD=802.11bgn,AUTH-MODE=WPAPSK/WPA2PSK,ENCRYP-TYPE=TKIPAES;'.encode())
                                        time.sleep(1) 
                                        rcv = s.recv(4096)
                                        retorno = rcv.decode()
                                        
                                        if 'DENY' in retorno:
                                            print(f"Erro ao Autorizar a ONU: {serial_onu1}")
                                        else:
                                            print(f"Sucesso ao Autorizar a ONU: {serial_onu1}")
                                    except:
                                        pass

                            except:
                               pass
    
                        else:
                            print("ONU Em bridge")
                except:
                   pass

        elif modelo_onu == 'AN5506-02-F':

            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-1')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan1 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 1: {vlan1}')
                vlan_lan1 = vlan1
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-1:CTAG::CVLAN={vlan_id_pon_destino},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 1 em Bridge ONU: {serial_onu1}")
            except:

                vlan_lan1 = ''
                pass

            
            try:
                s.send(f'LST-PORTVLAN::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-2:CTAG::;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                retorno = retorno.split()
                localiza = retorno.index('NA-NA-NA-2')
                localiza = localiza+2
                vlan_final = localiza+1
                vlan = retorno[localiza:vlan_final]
                vlan = str(vlan)
                vlan2 = vlan.replace("'",'').replace('[','').replace(']','').replace(',','.')
                print(f'VLAN LAN 2: {vlan2}')
                vlan_lan2 = vlan2
                s.send(f'CFG-LANPORTVLAN::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1},ONUPORT=NA-NA-NA-2:CTAG::CVLAN={vlan_lan2},CCOS=0;'.encode())
                time.sleep(1) 
                rcv = s.recv(4096)
                retorno = rcv.decode()
                if 'DENY' in retorno:
                    print(f"Erro ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
                else:
                    print(f"Sucesso ao Configurar a LAN 2 em Bridge ONU: {serial_onu1}")
                
            except:
                vlan_lan2 = ''
                pass
            
            
            if vlan_lan1 == '' and vlan_lan2 == '':
                
                print("Verificando WAN Service")
                try:
                    s.send(f'LST-ONUWANSERVICECFG::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1},PORTID=NA-NA-NA-1:CTAG::;'.encode())
                    time.sleep(0.5) 
                    rcv = s.recv(4096)
                    retorno = rcv.decode()
                    if  'DENY' in retorno:
                       pass
                    else:
                        if 'route' in retorno:    
                            print("ONU em Router")
                            localizar = retorno.split()
                            vlan_pppoe = localizar.index("INTERNET")
                            vlan_pppoe = vlan_pppoe + 2
                            vlan_final = vlan_pppoe + 1
                            vlan = localizar[vlan_pppoe:vlan_final]
                            vlan = str(vlan)
                            vlan = vlan.replace("'",'').replace('[','').replace(']','')
                            modo = localizar[vlan_final:]
                            modo_conexao = vlan_final + 2
                            modo_conexao_fim = modo_conexao + 1
                            login_pppoe_inicio = modo_conexao + 15
                            login_pppoe_fim = login_pppoe_inicio + 1
                            login_pppoe = localizar[login_pppoe_inicio:login_pppoe_fim]
                            login_pppoe = str(login_pppoe)
                            login_pppoe = login_pppoe.replace("'",'').replace('[','').replace(']','')
                            senha_pppoe_inicio = login_pppoe_fim
                            senha_pppoe_fim = senha_pppoe_inicio + 1
                            senha_pppoe = localizar[senha_pppoe_inicio:senha_pppoe_fim]
                            senha_pppoe = str(senha_pppoe)
                            senha_pppoe = senha_pppoe.replace("'",'').replace('[','').replace(']','')
                            modo_conexao = localizar[modo_conexao:modo_conexao_fim]
                            modo_conexao = str(modo_conexao)
                            modo_conexao = modo_conexao.replace("'",'').replace('[','').replace(']','')
                            bind_of_ports = localizar.index("33024")
                            bind_inicio = bind_of_ports + 5
                            bind_final = bind_inicio + 1
                            portas_bind = localizar[bind_inicio:bind_final]
                            portas_bind = str(portas_bind)
                            portas_bind = portas_bind.replace("-",' ')
                            portas_bind = portas_bind.replace("'",'').replace('[','').replace(']','')


                            
                            print(f'VLAN PPPoE: {vlan}')
                            print(f'Modo de conexão: {modo_conexao}')
                            print(f'Login PPPoE: {login_pppoe}')
                            print(f'Senha PPPoE: {senha_pppoe}')
                            print(f'Porta bindadas: {portas_bind}')
 
                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,UPORT=0;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service LAN na ONU: {serial_onu1}")
                            except:
                                pass

                            #Configurar WAN Service
                            try:
                                s.send(f'SET-WANSERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::STATUS=1,MODE=2,CONNTYPE=2,VLAN={vlan_id_pon_destino},COS=0,QOS=2,NAT=1,IPMODE=3,IPSTACKMODE=1,IP6SRCTYPE=1,PPPOEPROXY=2,PPPOEUSER={login_pppoe},PPPOEPASSWD={senha_pppoe},PPPOENAME=,PPPOEMODE=1,UPNP=1,SSID=1;'.encode())
                                time.sleep(1) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                
                                if 'DENY' in retorno:
                                    print(f"Erro ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                                else:
                                    print(f"Sucesso ao configurar a WAN Service WLAN 2.4GHZ na ONU: {serial_onu1}")
                            except:
                                pass


                            print("\nVerificando WIFI Service")
                   
                            try:
                                s.send(f'LST-WIFISERVICE::OLTID={ip_olt_origem},PONID=NA-NA-{slot_number_origem}-{pon_number_origem},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::;'.encode())
                                time.sleep(0.5) 
                                rcv = s.recv(4096)
                                retorno = rcv.decode()
                                if  'DENY' in retorno:
                                   pass
                                else:

                                    retorno = retorno.split()
                                    senha_24ghz = retorno[53]
                                    ssid_24ghz = retorno[48]
                                    
                                    print(f'SSID 2.4Ghz: {ssid_24ghz}')
                                    print(f'Senha 2.4Ghz: {senha_24ghz}')
                                    
                                    #Configurar WIFI

                                    try:
                                        s.send(f'CFG-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}::ENABLE=enable,WILESSAREA=5,WILESSCHANNEL=0,WILESSSTANDARD=802.11bgn,WORKINGFREQUENCY=2.4GHZ,T-POWER=140,SSID=1,SSIDENABLE=0,SSIDNAME={ssid_24ghz},SSIDVISIBALE=1,AUTHMODE=WPAPSK,ENCRYPTYPE=TKIP,PRESHAREDKEY={senha_24ghz},UPDATEKEYINTERVAL=3600,FREQUENCYBANDWIDTH=20/40MHZ;'.encode())
                                        time.sleep(1) 
                                        rcv = s.recv(4096)
                                        retorno = rcv.decode()
                                        
                                        if 'DENY' in retorno:
                                            print(f"Erro ao Configurar a ONU: {serial_onu1}")
                                        else:
                                            print(f"Sucesso ao Configurar a ONU: {serial_onu1}")                                    
                                    except:
                                        pass                                    
                                    
                                    try:
                                        s.send(f'MODIFY-WIFISERVICE::OLTID={ip_olt_destino},PONID=NA-NA-{slot_number_destino}-{pon_number_destino},ONUIDTYPE=MAC,ONUID={serial_onu1}:CTAG::WORKING-FREQUENCY=2.4Ghz,FREQUENCY-BANDWIDTH=20/40MHZ,ENABLE=enable,SSID-ENABLE=1,SSID-NAME={ssid_24ghz},PRESHARED-KEY={senha_24ghz},SSID=1,WILESS-STANDARD=802.11bgn,AUTH-MODE=WPAPSK/WPA2PSK,ENCRYP-TYPE=TKIPAES;'.encode())
                                        time.sleep(1) 
                                        rcv = s.recv(4096)
                                        retorno = rcv.decode()
                                        
                                        if 'DENY' in retorno:
                                            print(f"Erro ao Autorizar a ONU: {serial_onu1}")
                                        else:
                                            print(f"Sucesso ao Autorizar a ONU: {serial_onu1}")
                                    except:
                                        pass
                            except:
                               pass
                    
                        else:
                            print("ONU Em bridge")
                except:
                   pass
            
            
        
        else:
            print("Outro Modelo")
            
            print("Verificar o script...")
            pause_app = input("Pressione alguma tecla para continuar...")

            
        print("=="*30)

        
        print('\n')


tempo_final = time.time()

print(f"{tempo_final - tempo_inicial} segundos")
            

numero_linhas = int(numero_linhas)            
            
print(f"\n\nLinhas analisadas: {numero_linhas}")

s.send('LOGOUT:::CTAG::;'.encode())
time.sleep(0.5) 
rcv = s.recv(4096)
retorno = rcv.decode()  
        
print('---'*30)


dataBase.close()


pause_app = input("Pressione alguma tecla para continuar")
