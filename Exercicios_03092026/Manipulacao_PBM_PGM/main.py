arquivo = open("Entrada_EscalaCinza.pgm")

#leitura do tipo
tipo = arquivo.readline().strip()

#leitura das dimensoes
dimensoes = arquivo.readline().strip().split()

largura = int(dimensoes[0])
altura = int(dimensoes[1])

#le o valor maximo
valor_maximo = int(arquivo.readline().strip())

#le pixels
pixels = arquivo.read().split()

#converte pixels para int
pixels = [int(pixel) for pixel in pixels]

arquivo.close()

#limiar
limiar = 128

#converte a imagem para preto e branco
pixels_pb = []

for pixel in pixels:
    if pixel <= limiar:
        pixels_pb.append(0)
    else:
        pixels_pb.append(1)
        

#cria arquivo pbm
saida = open("SaidaPBM.pbm", "w")

#cabecalho
saida.write("P1\n")
saida.write(str(largura) + " " + str(altura) + "\n")

#escreve os pixels
for pixel in pixels_pb:
    saida.write(str(pixel) + "\n")
    

saida.close()

print("Imagem PBM criada com sucesso!")