arquivo_entrada = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Exercicios_03092026\CanaisCores\Fig4.ppm"

arquivo_saida_r_min = "Fig4_R_Min.ppm"
arquivo_saida_g_min = "Fig4_G_Min.ppm"
arquivo_saida_b_min = "Fig4_B_Min.ppm"

arquivo_saida_r_max = "Fig4_R_Max.ppm"
arquivo_saida_g_max = "Fig4_G_Max.ppm"
arquivo_saida_b_max = "Fig4_B_Max.ppm"


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


pixels_r_min = []
pixels_g_min = []
pixels_b_min = []

pixels_r_max = []
pixels_g_max = []
pixels_b_max = []


indice = 0

while indice < len(pixels):

    vermelho = int(pixels[indice])
    verde = int(pixels[indice + 1])
    azul = int(pixels[indice + 2])


    #R - Minimo
    pixels_r_min.append(str(vermelho))
    pixels_r_min.append("0")
    pixels_r_min.append("0")


    #G - Minimo
    pixels_g_min.append("0")
    pixels_g_min.append(str(verde))
    pixels_g_min.append("0")


    #B - Minimo
    pixels_b_min.append("0")
    pixels_b_min.append("0")
    pixels_b_min.append(str(azul))


    #R - Maximo
    pixels_r_max.append(str(vermelho))
    pixels_r_max.append("255")
    pixels_r_max.append("255")


    #G - Maximo
    pixels_g_max.append("255")
    pixels_g_max.append(str(verde))
    pixels_g_max.append("255")


    #B - Maximo
    pixels_b_max.append("255")
    pixels_b_max.append("255")
    pixels_b_max.append(str(azul))


    indice = indice + 3


#IMAGEM 1 - R MINIMO
with open(arquivo_saida_r_min, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_r_min:
        arquivo.write(pixel + "\n")


#IMAGEM 2 - G MINIMO
with open(arquivo_saida_g_min, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_g_min:
        arquivo.write(pixel + "\n")


#IMAGEM 3 - B MINIMO
with open(arquivo_saida_b_min, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_b_min:
        arquivo.write(pixel + "\n")


#IMAGEM 4 - R MAXIMO
with open(arquivo_saida_r_max, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_r_max:
        arquivo.write(pixel + "\n")


#IMAGEM 5 - G MAXIMO
with open(arquivo_saida_g_max, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_g_max:
        arquivo.write(pixel + "\n")


#IMAGEM 6 - B MAXIMO
with open(arquivo_saida_b_max, "w") as arquivo:

    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    for pixel in pixels_b_max:
        arquivo.write(pixel + "\n")


print("Processamento concluído.")