import os
import random
from threading import *
import time
# from collections import OrderedDict

x, y, w, z = 4, 12, 1000, 1400
correndo = []
atual_correndo = []
total_de_voltas = {}
carros = ["C1", "C2"]
escuderias = ["E1", "E2", "E3", "E4", "E5", "E6"]
semaforoEscuderia = Semaphore(1)
semaforoCarros = Semaphore(5)


def tempo_rand(a, b):
    return random.randint(a, b)


# Verifica se o tempo total de execução do programa passou dos 60 segundos
def verifica_tempo(tempo_total_programa, total_de_voltas):
    if tempo_total_programa > 60:
        print("\nFim da corrida após 60 segundos.")
        imprime_resultado_final(total_de_voltas)


# Calcula e verifica o tempo do segundo ciclo de voltas
def tempo_segunda_volta(tmp_volta):
    variacao = random.randint(-10, 10)
    tmp_volta = tmp_volta + (tmp_volta * variacao / 100)
    if tmp_volta < 1000:
        tmp_volta = 1000
    elif tmp_volta > 1400:
        tmp_volta = 1400
    return tmp_volta


def imprime_resultado_final(total_de_voltas):
    print('')
    for key in total_de_voltas:
        #        print(OrderedDict(sorted(total_de_voltas.items())))
        print(
            f"O carro {key} fez {total_de_voltas[key][1]} voltas, em {total_de_voltas[key][0]} ciclos de voltas, em um tempo de {int(total_de_voltas[key][2] * 1000)} milissegundos.")
    os._exit(1)


def verifica_soma(total_de_voltas, atual_correndo):
    verifica_tempo(time.process_time(), total_de_voltas)
    soma = 0
    faixa = len(total_de_voltas)
    for i in range(0, faixa):
        soma = soma + list(total_de_voltas.items())[i][1][0]
        if soma == 24 and len(atual_correndo) == 0:
            imprime_resultado_final(total_de_voltas)


def pista(escuderia, id, num_voltas, tmp_volta):
    # Verifica se já há algum carro daquela escuderia correndo
    if escuderia not in correndo and len(correndo) < 6:
        nome_carro = escuderia + id

        # Verifica se o carro já está registrado no dicionário "total_de_voltas"
        if nome_carro not in total_de_voltas:
            verifica_tempo(time.process_time(), total_de_voltas)
            correndo.append(escuderia)
            atual_correndo.append(nome_carro)
            total_de_voltas[nome_carro] = 1, num_voltas, round((num_voltas * tmp_volta) / 1000, 2)
            semaforoCarros.acquire()
            print(f'\nCarro {escuderia + id} entrou na pista.')
            print(f'Atualmente correndo: {atual_correndo}')
            time.sleep(num_voltas * (tmp_volta / 1000))
            semaforoCarros.release()
            correndo.remove(escuderia)
            atual_correndo.remove(nome_carro)
            print(
                f'Carro {nome_carro} fez {num_voltas} voltas em {round((num_voltas * tmp_volta) / 1000, 2)} segundos e saiu da pista.')

        # Carro já fez pelo menos 1 volta
        elif total_de_voltas[nome_carro][0] < 2:
            verifica_tempo(time.process_time(), total_de_voltas)
            tempo_total = round(total_de_voltas[nome_carro][2] + (num_voltas * tmp_volta) / 1000, 2)
            numero_total_voltas = total_de_voltas[nome_carro][1] + num_voltas
            correndo.append(escuderia)
            atual_correndo.append(nome_carro)
            total_de_voltas[nome_carro] = 2, numero_total_voltas, tempo_total
            semaforoCarros.acquire()
            print(f'\nCarro {escuderia + id} entrou na pista.')
            print(f'Atualmente correndo: {atual_correndo}')
            time.sleep(num_voltas * (tempo_segunda_volta(tmp_volta) / 1000))
            semaforoCarros.release()
            correndo.remove(escuderia)
            atual_correndo.remove(nome_carro)
            print(
                f'Carro {nome_carro} fez {num_voltas} voltas em {round((num_voltas * tmp_volta) / 1000, 2)} segundos e saiu da pista.')
            verifica_soma(total_de_voltas, atual_correndo)


def esc(id):
    semaforoEscuderia.acquire()
    E1 = Thread(target=pista, args=('E1', id, tempo_rand(x, y), tempo_rand(w, z)))
    E2 = Thread(target=pista, args=('E2', id, tempo_rand(x, y), tempo_rand(w, z)))
    E3 = Thread(target=pista, args=('E3', id, tempo_rand(x, y), tempo_rand(w, z)))
    E4 = Thread(target=pista, args=('E4', id, tempo_rand(x, y), tempo_rand(w, z)))
    E5 = Thread(target=pista, args=('E5', id, tempo_rand(x, y), tempo_rand(w, z)))
    E6 = Thread(target=pista, args=('E6', id, tempo_rand(x, y), tempo_rand(w, z)))

    if random.choice(escuderias) == "E1":
        E1.start()
    elif random.choice(escuderias) == "E2":
        E2.start()
    elif random.choice(escuderias) == "E3":
        E3.start()
    elif random.choice(escuderias) == "E4":
        E4.start()
    elif random.choice(escuderias) == "E5":
        E5.start()
    elif random.choice(escuderias) == "E6":
        E6.start()
    semaforoEscuderia.release()


while True:
    C1 = Thread(target=esc, args=('C1',))
    C2 = Thread(target=esc, args=('C2',))
    if random.choice(carros) == "C1":
        C1.start()
    else:
        C2.start()
