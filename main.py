# -*- coding: utf-8 -*-

import sys
import time

from conexao import Conexao
from funcoes import *

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

dia_formato_texto = datetime.now().strftime("%A")

dias_da_semana = {
    'segunda-feira': 2,
    'terÃ§a-feira': 3,
    'quarta-feira': 4,
    'quinta-feira': 5,
    'sexta-feira': 6,
    'sábado': 7,
    'domingo': 1
}

numero_dia = dias_da_semana.get(dia_formato_texto)
if not numero_dia:
    print("Tentando outra forma de validar dia")
    numero_dia = dias_da_semana.get(f"{dia_formato_texto}-feira")

def main():
    tocar_som("sons/reset.mp3")
    print("Conectando-se com o Banco de Dados")
    time.sleep(2)
    obj1 = Conexao("127.0.0.1", "root", "")
    res = obj1.conectar()
    if not res:
        print("Tentando outro login de conexão")
        time.sleep(2)
        obj2 = Conexao("127.0.0.1", "root", "root")
        obj3 = Conexao("127.0.0.1", "root", "Cefet123")
        obj4 = Conexao("127.0.0.1", "root", "cefet123")
        lsObjeto = [obj2, obj3, obj4]
        lsConexaoObjeto = [obj2.conectar(), obj3.conectar(), obj4.conectar()]

        for i, valor in enumerate(lsConexaoObjeto):
            if valor:
                res = lsObjeto[i]
                break
            if i == len(lsConexaoObjeto) - 1:
                print("\nTodos os métodos de conexão ao Banco de Dados falharam.")
                time.sleep(2)
                print("\nfechando...")
                time.sleep(3)
                sys.exit()
    else:
        res = obj1

    if acessar_hora_web():
        hora_agora = acessar_hora_web().time()
        print("\nHora obtida do servidor Google\n")
    else:
        hora_agora = datetime.now().time()
        print("\nHora obtida localmente\n")
    disciplina_encontrada = []

    cond = 1 # <-- flag do meu programa

    while cond == 1:
        print_uma_vez = 0
        siape = input("Digite o seu siape para logon: \n>")
        print("\n")
        siape_concat = f"{siape}MASTER"

        resultados_consulta = res.destranca_sistema(siape_concat)
        tocar_som("sons/beep.mp3")
        if resultados_consulta:

            for valor in resultados_consulta:
                horario = valor[4].split("-")
                horario_inicial = horario[0]
                horario_final = horario[1]

                horario_inicial_time = converter_hora_string(horario_inicial)
                horario_final_time = converter_hora_string(horario_final)

                dia = int(valor[5])
                data_agora = valor[6]

                if horario_inicial_time <= hora_agora <= horario_final_time and int(numero_dia) == dia and acessar_data() == data_agora :
                    disciplina_encontrada.append(valor[0])
                    disciplina_encontrada.append(valor[1])
                    disciplina_encontrada.append(valor[2])
                    disciplina_encontrada.append(valor[3])
                    disciplina_encontrada.append(valor[4])
                    disciplina_encontrada.append(valor[5])
                    print(f"Bem vindo, {valor[1]}")
                    cond = 0

                    break
                elif horario_inicial_time <= hora_agora <= horario_final_time and int(numero_dia) != dia or acessar_data() != data_agora:
                    print_uma_vez += 1
                    if print_uma_vez == 1:
                        ...
                        print("Sessão não foi aberta\n")
                elif (horario_inicial_time > hora_agora or hora_agora > horario_final_time) and int(numero_dia) == dia or acessar_data() == data_agora:
                    print_uma_vez += 1
                    if print_uma_vez == 1:
                        print("Não está dentro do seu horário \n")

                    #break
                else:
                    print_uma_vez += 1
                    if print_uma_vez == 1:
                        print("Dia e Horário incompatíveis \n")
        else:
            print("SIAPE informado incorretamente devido a um erro de leitura no cartão \n")
    lista_sessao_inicial = []
    lista_sessao_final = []

    while True:
        aluno = input("Digite a matrícula do aluno: \n>")
        horario_completo = disciplina_encontrada[4].split("-")
        hora_inicial = horario_completo[0]
        hora_final = horario_completo[1]

        hi = converter_hora_string(hora_inicial)
        hf = converter_hora_string(hora_final)
        hi_limite = (datetime.combine(datetime.today(), hi) + timedelta(minutes=20)).time()
        hf_limite = (datetime.combine(datetime.today(), hf) - timedelta(minutes=20)).time()

        tempo_datetime_agora = datetime.combine(datetime.today(), hora_agora)
        tempo_final_aula = datetime.combine(datetime.today(), hf)
        tempo_limite_sessao = datetime.combine(datetime.today(), hf) + timedelta(minutes=2)
        if tempo_final_aula < tempo_datetime_agora < tempo_limite_sessao or aluno == "EVILKEY":
            disciplina_encontrada.clear()
            lista_sessao_inicial.clear()
            lista_sessao_final.clear()
            main()
            break
        if aluno == "Check":
            dados = ""
            print("\n")
            for i, aluno_inicial in enumerate(lista_sessao_inicial):
                valorConsulta = res.ver_sobre_aluno(aluno_inicial, disciplina_encontrada[2], str(acessar_data()))

                try:
                    data_hora = converter_para_padrao_brasil(str(valorConsulta[4]))
                    print(f"Aluno, {valorConsulta[0]} passou pela ultima vez às:  '{data_hora}', inscrito na matricula: {valorConsulta[1]}\n")
                    dados += f"Aluno, {valorConsulta[0]} passou pela ultima vez às:  '{data_hora}', inscrito na matricula: {valorConsulta[1]}\n"
                    with open("controle.txt", "w+", encoding="utf-8") as arqEscrita:
                        arqEscrita.write(dados)
                        arqEscrita.flush()
                    tocar_som("sons/ping.mp3")
                except:
                    print("Ocorreu algum erro\n")
                    tocar_som("sons/beep.mp3")
        else:
            tocar_som("sons/beep.mp3")
            print(f"{hi} --> Horário Atual: {hora_agora}, até o limite da sessão inicial <-- {hi_limite}")
            if hi <= hora_agora <= hi_limite and aluno.lower() not in lista_sessao_inicial:
                print(res.marcar_presenca(aluno, disciplina_encontrada, acessar_data()))
                lista_sessao_inicial.append(aluno.lower())
            elif hf_limite <= hora_agora <= hf and aluno.lower() not in lista_sessao_final:
                print(f"{hf_limite} <= {hora_agora} <= {hf}")
                print(res.marcar_presenca(aluno, disciplina_encontrada, acessar_data()))
                lista_sessao_final.append(aluno.lower())
            elif aluno.lower() in lista_sessao_inicial or aluno.lower() in lista_sessao_final:
                print("Você já passou o cartão \n")
            else:
                print("Fora do Horário \n")

main()
