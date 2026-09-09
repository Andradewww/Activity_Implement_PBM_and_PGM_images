arquivo_entrada = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Exercicios_03092026\ImagemRgbMedia\Fig4.ppm"
arquivo_saida_p2 = "Fig4_P2.pgm"
arquivo_saida_p3 = "Fig4_media.ppm"


with open(arquivo_entrada, "r") as arquivo:
    linhas = arquivo.readlines()


dados = []

for linha in linhas:

    linha = linha.strip()

    if linha == "":
        continue

    if linha.startswith("#"):
        continue

    dados.extend(linha.split())


tipo = dados[0]
largura = int(dados[1])
altura = int(dados[2])
valor_maximo = int(dados[3])


if tipo != "P3":
    print("Erro: o arquivo não está no formato P3.")
    exit()


pixels = dados[4:]

pixels_p2 = []
pixels_p3 = []


indice = 0

while indice < len(pixels):

    vermelho = int(pixels[indice])
    verde = int(pixels[indice + 1])
    azul = int(pixels[indice + 2])

    media = int((vermelho + verde + azul) / 3)

    pixels_p2.append(str(media))

    pixels_p3.append(str(media))
    pixels_p3.append(str(media))
    pixels_p3.append(str(media))

    indice = indice + 3


with open(arquivo_saida_p2, "w") as arquivo:

    arquivo.write("P2\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_p2:
        arquivo.write(pixel + "\n")


with open(arquivo_saida_p3, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_p3:
        arquivo.write(pixel + "\n")


print("Processamento concluído.")