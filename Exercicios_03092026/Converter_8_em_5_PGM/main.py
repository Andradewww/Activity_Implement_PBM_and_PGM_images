arquivo = open("EntradaEscalaCinza.pgm", "r")

#verificamos o tipo da imagem
tipo = arquivo.readline().strip()

#verificamos as dimensões
dimensoes = arquivo.readline().strip().split()

largura = int(dimensoes[0])
altura = int(dimensoes[1])

#valor máximo dos pixels
valor_maximo = int(arquivo.readline().strip())

#leitura dos pixels
pixels = arquivo.read().split()

#convertemos pixel para inteiro
pixels = [int(pixel) for pixel in pixels]

arquivo.close()


print("Tipo:", tipo)
print("Largura:", largura)
print("Altura:", altura)
print("Valor máximo:", valor_maximo)
print("Quantidade de pixels:", len(pixels))


#conversão de 8 bits para 5 bits
pixels_5_bits = []

for pixel in pixels:
    novo_pixel = int(pixel * 31 / 255)
    pixels_5_bits.append(novo_pixel)


print("Primeiros pixels originais:", pixels[:10])
print("Primeiros pixels convertidos:", pixels_5_bits[:10])


#cria o arquivo de saída
saida = open("Saida5Bits.pgm", "w")

#escreve o cabeçalho da imagem
saida.write("P2\n")
saida.write(str(largura) + " " + str(altura) + "\n")
saida.write("31\n")

#escreve os pixels convertidos
for pixel in pixels_5_bits:
    saida.write(str(pixel) + "\n")

saida.close()

print("Imagem convertida salva com sucesso!")