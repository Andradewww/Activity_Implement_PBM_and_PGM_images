arquivo = open("Entrada_EscalaCinza.pgm", "r")

#leitura do tipo
tipo = arquivo.readline().strip()

#leitura da dimensao
dimensoes = arquivo.readline().strip().split()

largura = int(dimensoes[0])
altura = int(dimensoes[1])

#le o valor maximo
valor_maximo = int(arquivo.readline().strip())

#le os pixels
pixels = arquivo.read().split()

#converte os pixels para inteiro
pixels = [int(pixel) for pixel in pixels]

arquivo.close()


#limiar
limiar = 128

#imagem para binario
pixels_binarizados = []

for pixel in pixels:

    if pixel <= limiar:
        pixels_binarizados.append(0)
    else:
        pixels_binarizados.append(255)


#cria arquivo de saida
saida = open("SaidaBin.pgm", "w")

#cabecalho PGM P2
saida.write("P2\n")
saida.write(str(largura) + " " + str(altura) + "\n")
saida.write("255\n")

#escreve os pixels
for pixel in pixels_binarizados:
    saida.write(str(pixel) + "\n")

saida.close()

print("Imagem PGM binarizada criada com sucesso!")