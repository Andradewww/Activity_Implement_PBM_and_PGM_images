import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import os

#leitura da imagem PGM
def ler_pgm(nome_arquivo):

    arquivo = open(nome_arquivo, "r")
    linhas = arquivo.readlines()
    arquivo.close()
    dados = []

    for linha in linhas:

        linha = linha.strip()

        if linha == "":
            continue

        if linha.startswith("#"):
            continue
        
        partes = linha.split()

        for parte in partes:
            dados.append(parte)

    tipo = dados[0]

    if tipo != "P2":
        print("Erro: o arquivo não é um PGM P2.")
        return None

    #dimensoes
    largura = int(dados[1])
    altura = int(dados[2])

    valor_maximo = int(dados[3])
    pixels = []

    for i in range(4, len(dados)):
        pixels.append(int(dados[i]))

    return largura, altura, valor_maximo, pixels


#salvar imagem PGM
def salvar_pgm(nome_arquivo, largura, altura, valor_maximo, pixels):

    arquivo = open(nome_arquivo, "w")
    arquivo.write("P2\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    contador = 0

    for pixel in pixels:
        arquivo.write(str(pixel) + " ")
        contador += 1

        if contador == largura:
            arquivo.write("\n")
            contador = 0

    arquivo.close()


#encontrar XMIN E XMAX
def encontrar_min_max(pixels):

    xmin = pixels[0]
    xmax = pixels[0]

    for pixel in pixels:

        if pixel < xmin:
            xmin = pixel

        if pixel > xmax:
            xmax = pixel

    return xmin, xmax

#transformacao linear
# Y = a * X + b
# a = 255 / (Xmax - Xmin)
# b = -a * Xmin

def realce_linear(pixels):

    #encontra XMIN e XMAX
    xmin, xmax = encontrar_min_max(pixels)

    print("Xmin =", xmin)
    print("Xmax =", xmax)

    #verifica se todos os pixels possuem o mesmo valor
    if xmax == xmin:

        print("A imagem possui apenas um nível de cinza.")
        return pixels

    #calculo do parametro A
    a = 255.0 / (xmax - xmin)

    #calcula o parametro B
    b = -a * xmin

    print("a =", a)
    print("b =", b)

    pixels_saida = []

    #aplica Y = aX + b em cada pixel
    for x in pixels:

        y = a * x + b

        #converte para inteiro
        y = int(round(y))

        #garante que fique entre 0 e 255
        if y < 0:
            y = 0

        if y > 255:
            y = 255

        pixels_saida.append(y)

    return pixels_saida


#histograma
def calcular_histograma(pixels):

    #cria 256 posicoes, uma para cada nível de cinza
    histograma = [0] * 256

    #conta quantos pixels existem em cada nivel
    for pixel in pixels:

        histograma[pixel] += 1

    return histograma


#gerar grafico do histograma
def gerar_grafico_histograma(histograma, titulo, nome_arquivo):

    #valores de 0 até 255
    niveis = []

    for i in range(256):
        niveis.append(i)

    plt.figure()

    plt.bar(niveis, histograma, width=1)

    plt.title(titulo)
    plt.xlabel("Nível de cinza")
    plt.ylabel("Quantidade de pixels")

    plt.xlim(0, 255)

    plt.savefig(nome_arquivo)

    plt.show()


# PROGRAMA PRINCIPAL --------------------------------------

# pasta onde está o Main.py
pasta_programa = os.path.dirname(os.path.abspath(__file__))

# pasta Img
pasta_img = os.path.join(pasta_programa, "Img")

# arquivo de entrada
arquivo_entrada = os.path.join(
    pasta_img,
    "Entrada_EscalaCinza.pgm"
)

# arquivo de saída
arquivo_saida = os.path.join(
    pasta_img,
    "Saida_EscalaCinza.pgm"
)

#leitura da imagem
resultado = ler_pgm(arquivo_entrada)

if resultado is not None:

    largura, altura, valor_maximo, pixels = resultado

    print("----------------------------------")
    print("Imagem PGM")
    print("----------------------------------")
    print("Largura:", largura)
    print("Altura:", altura)
    print("Valor máximo:", valor_maximo)
    print("Quantidade de pixels:", len(pixels))

    #histograma da imagem original
    histograma_original = calcular_histograma(pixels)

    gerar_grafico_histograma(
        histograma_original,
        "Histograma - Imagem Original",
        os.path.join(pasta_img, "Histograma_Original.png")
    )

    #realce linear

    pixels_saida = realce_linear(pixels)

    #salvar imagem realcada

    salvar_pgm(
        arquivo_saida,
        largura,
        altura,
        255,
        pixels_saida
    )

    print("----------------------------------")
    print("Imagem realçada salva em:")
    print(arquivo_saida)


    #histograma da imagem realcada
    
    histograma_realce = calcular_histograma(pixels_saida)

    gerar_grafico_histograma(
        histograma_realce,
        "Histograma - Imagem Realçada",
        os.path.join(pasta_img, "Histograma_Realce.png")
    )

    print("----------------------------------")
    print("Processamento concluído!")