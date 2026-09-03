arquivo = open("../Converter_8_em_5_PGM/Saida5Bits.pgm", "r")

#leitura da imagem
tipo = arquivo.readline().strip()

#leitura das dimensões
dimensioes = arquivo.readline().strip().split()

largura = int(dimensioes[0])
altura = int(dimensioes[1])

#lê o valor máximo
valor_maximo = int(arquivo.readline().strip())

#lê os pixels
pixels = arquivo.read().split()

#converte pixel para inteiro
pixels = [int(pixel) for pixel in pixels]

arquivo.close()


#aplicando ganho de 20% de claridade
pixels_claros = []

for pixel in pixels:
    novo_pixel = int(pixel * 1.2)
    
    #não permite que o valor passe de 31
    if novo_pixel > 31:
        novo_pixel = 31
        
    pixels_claros.append(novo_pixel)
    

#cria imagem de saída
saida = open("SaidaBrilho.pgm", "w")

#cabecalho
saida.write("P2\n")
saida.write(str(largura) + " " + str(altura) + "\n")
saida.write("31\n")

#pixels
for pixel in pixels_claros:
    saida.write(str(pixel) + "\n")
    
saida.close()

print("Imagem com 20% de claridade salva com sucesso!")