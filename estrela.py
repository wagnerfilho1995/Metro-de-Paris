#-*- coding: utf-8 -*-
#	INFORMAÇÕES DO PROBLEMA
# VELOCIDADE MEDIA DE UM TREM = 30km/h
# TEMPO MÉDIO PARA TROCAR DE ESTAÇÃO = 4 mins

# ARRAY COM NOME DAS ESTAÇÕES DO MAPA
E = ["La Défense", "Charles de Gaulle Étoile", "Concorde", "Palais Royal Musée du Louvre", "Reuilly-Diderot", 
	"Daumesnil", "Gare de Lyon", "Barbès Rochechouart", "Place de Clichy", "Victor Hugo", "Gabriel Péri",
	"Porte de Clignancourt", "Denfert Rochereau", "Porte d'Orléans"]

# LISTA REPRESENTANDO A FRONTEIRA USADA PARA A BUSCA DO A*
fronteira = []

# ARRAY AUXILIAR PARA MARCAÇÃO DE ESTAÇÕES JÁ OU NÃO VISITADAS
visitados = [0]*14

resposta = []

trocasDeEstacao = 0
km = 0

#	PEGAR ESTAÇÃO INICIAL QUE O PASSAGEIRO SE ENCONTRA
def partida():
	print("Informe sua Estação:")
	for i in range(0, len(E)):
		print("{} - {}".format(i+1, E[i]))
	p = int(input())-1
	if(p < 0 or p > 14):
		print("Por favor, selecione o número de uma das estações abaixo:")
		partida()
	return p

#	PEGAR DESTINO FINAL DO PASSAGEIRO
def chegada():
	print("Informe seu Destino:")
	for i in range(0, len(E)):
		print("{} - {}".format(i+1, E[i]))
	c = int(input())-1
	return c


# TABELA DE DISTANCIAS EM LINHA RETA
H = [
#	 E1  E2  E3  E4  E5  E6  E7  E8  E9 E10  E11 E12 E13 E14
	(0,  11, 20, 27, 40, 43, 39, 28, 18, 10, 18, 30, 30, 32),# E1
	(11,  0,  9, 16, 29, 32, 28, 19, 11,  4, 17, 23, 21, 24),# E2
	(20,  9,  0,  7, 20, 22, 19, 15, 10, 11, 21, 21, 13, 18),# E3
	(27, 16,  7,  0, 13, 16, 12, 13, 13, 18, 26, 21, 11, 17),# E4
	(40, 29, 20, 13,  0,  3,  2, 21, 25, 31, 38, 27, 16, 20),# E5
	(43, 32, 22, 16,  3,  0,  4, 23, 28, 33, 41, 30, 17, 20),# E6
	(39, 28, 19, 12,  2,  4,  0, 22, 25, 29, 38, 28, 13, 17),# E7
	(28, 19, 15, 13, 21, 23, 22,  0,  9, 22, 18,  7, 25, 30),# E8
	(18, 11, 10, 13, 25, 28, 25,  9,  0, 13, 12, 12, 23, 28),# E9
	(10,  4, 11, 18, 31, 33, 29, 22, 13,  0, 20, 27, 20, 23),# E10
	(18, 17, 21, 26, 38, 41, 38, 18, 12, 20,  0, 15, 35, 39),# E11
	(30, 23, 21, 21, 27, 30, 28,  7, 12, 27, 15,  0, 31, 37),# E12
	(30, 21, 13, 11, 16, 17, 13, 25, 23, 20, 35, 31,  0,  5),# E13
	(32, 24, 18, 17, 20, 20, 17, 30, 28, 23, 39, 37,  5,  0) # E14
	]

# AZUL     1
# AMARELA  2
# VERDE    3
# VERMELHA 4

# TABELA DE LIGAÇÕES, REPRESENTANDO TAMBEM A COR DA LINHA É FEITA A LIGAÇÃO
L = [
#	E0  E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13
	(0, 1,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E0
	(1, 0,  1, 0, 0, 0, 0, 0, 2,  2,  0,  0,  0,  0),# E1
	(0, 1,  0, 1, 0, 0, 0, 0, 4,  0,  0,  0,  4,  0),# E2
	(0, 0,  1, 0, 1, 0, 0, 3, 0,  0,  0,  0,  3,  0),# E3
	(0, 0,  0, 1, 0, 1, 2, 2, 0,  0,  0,  0,  0,  0),# E4
	(0, 0,  0, 0, 1, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E5
	(0, 0,  0, 0, 2, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E6
	(0, 0,  0, 3, 2, 0, 0, 0, 2,  0,  0,  3,  0,  0),# E7
	(0, 2,  4, 0, 0, 0, 0, 2, 0,  0,  4,  0,  0,  0),# E8
	(0, 2,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E9
	(0, 0,  0, 0, 0, 0, 0, 0, 4,  0,  0,  0,  0,  0),# E10
	(0, 0,  0, 0, 0, 0, 0, 3, 0,  0,  0,  0,  0,  0),# E11
	(0, 0,  4, 3, 0, 0, 0, 0, 0,  0,  0,  0,  0,  3),# E12
	(0, 0,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  3,  0) # E13
	]

def converterParaTempo(x):
	mins = x*2
	return mins

def corDasLinhas(cor):
	if cor == 1:
		return "Azul"
	elif cor == 2:
		return "Amarela"
	elif cor == 3:
		return "Verde"
	elif cor == 4:
		return "Vermelha"

def printar_fronteira():
	print("FRONTEIRA:")
	for i in range(0, len(fronteira)):
		if(visitados[fronteira[i][2]] == 0):
			print(fronteira[i])

def caminho(a):
	while a[3][2] != -1:
		resposta.append(a[3][2])
		a = a[3] 

def sucessores_de(a):
	for i in range (0, len(E)):
		if(L[a[2]][i] != 0 and visitados[a[2]] == 0):
			#	CALCULAR O G DESSE SUCESSOR
			g = converterParaTempo(a[3][1] + H[a[2]][i])
			#	CALCULAR H DESSE SUCESSOR
			h = converterParaTempo(H[i][pontoChegada])
			#	PAI DO SUCESSOR (DE QUE ESTAÇÃO ESSE TREM CHEGOU EM i)
			pai = a
			#	COR DA LINHA
			linha = L[a[2]][i]
			if(a[4] != linha):
				h += 4	#	ACRESCIMO DOS 4 MINUTOS NA TROCA DE LINHA
			#	ADICIONAR NA FRONTEIRA NOVO SUCESSOR
			s = [h+g, g, i, pai, linha]
			fronteira.append(s)
	visitados[a[2]] = 1

def estrela():
	k = 0
	while k > -1:	
		# AINDA NÃO CHEGAMOS...
		for i in range(0, len(fronteira)):
			if(visitados[fronteira[i][2]] == 0):
				break
		if(fronteira[i][2] == pontoChegada):
			visitados[fronteira[i][2]] = 1
			resposta.append(fronteira[i][2])
			caminho(fronteira[i])
			break
		sucessores_de(fronteira[i])
		fronteira.sort(key=lambda fronteira: fronteira[0])
		printar_fronteira()
		k += 1

# MAIN

pontoPartida = partida()
pontoChegada = chegada()

print("ESTADO INICIAL: {}".format(E[pontoPartida]))
print("ESTADO   FINAL: {}".format(E[pontoChegada]))

V = [0, 0, -1, -1, -1]

# E = [f, g, indiceEstacao, pai, corDaLinha]
a = [converterParaTempo(0 + H[pontoPartida][pontoChegada]), 0, pontoPartida, V, None]

fronteira.append(a)

estrela()

final = resposta[::-1] 

print("\n\nMelhor Caminho: E{} -> E{}".format(pontoPartida+1, pontoChegada+1))
for i in range (0, len(final)):
	if i == 0:
		print("Saindo da Estação: [E{} : {}] - (Linha: {}) ...\n".format(final[i]+1, E[final[i]], corDasLinhas(L[final[i]][final[i+1]])))
		km += (H[final[i]][final[i+1]])
	elif i == len(final)-1:
		print("...Chegando na Estação: [E{} : {}]\n".format(final[i]+1, E[final[i]]))
	else:
		km += H[final[i]][final[i+1]]
		if L[final[i-1]][final[i]] != L[final[i]][final[i+1]]:
			print(">> TROCA DE ESTAÇÃO! <<")
			trocasDeEstacao += 1
		print("...Vindo pela (Linha: {}) - Passando por [E{} : {}] - Indo pela (Linha: {}) ...\n".format(corDasLinhas(L[final[i-1]][final[i]]), final[i]+1, E[final[i]], corDasLinhas(L[final[i]][final[i+1]])))

print("Percorridos: {} km com {} troca(s) de Estação".format(km, trocasDeEstacao))
print("Tempo estimado: {} minutos".format(converterParaTempo(km) + 4*trocasDeEstacao))

