import matplotlib.pyplot as plt
import os

#leitura da imagem PPM
def ler_ppm(nome_arquivo):

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

    if tipo != "P3":
        print("Erro: o arquivo não é um PPM P3.")
        return None

    #dimensoes
    largura = int(dados[1])
    altura = int(dados[2])

    valor_maximo = int(dados[3])

    pixels = []

    for i in range(4, len(dados)):
        pixels.append(int(dados[i]))

    return largura, altura, valor_maximo, pixels


#salvar imagem PPM
def salvar_ppm(nome_arquivo, largura, altura, valor_maximo, pixels):

    arquivo = open(nome_arquivo, "w")
    arquivo.write("P3\n")
    arquivo.write(str(largura) + " " + str(altura) + "\n")
    arquivo.write(str(valor_maximo) + "\n")

    contador = 0

    for pixel in pixels:
        arquivo.write(str(pixel) + " ")
        contador += 1

        if contador % 3 == 0:
            arquivo.write("  ")

        if contador == largura * 3:
            arquivo.write("\n")
            contador = 0

    arquivo.close()


#encontra XMIN E XMAX
def encontrar_min_max(pixels):

    xmin = pixels[0]
    xmax = pixels[0]

    for pixel in pixels:

        if pixel < xmin:
            xmin = pixel

        if pixel > xmax:
            xmax = pixel

    return xmin, xmax


# realce linear - Y = a * X + b
# a = 255 / (Xmax - Xmin)
# b = -a * Xmin
def realce_linear(pixels):

    xmin, xmax = encontrar_min_max(pixels)

    print("Xmin =", xmin)
    print("Xmax =", xmax)

    if xmax == xmin:

        print("O canal possui apenas um nível de intensidade.")
        return pixels

    a = 255.0 / (xmax - xmin)

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


# REALCE LINEAR APLICADO À IMAGEM RGB
# Aplica a transformação linear em cada canal (R, G, B)

def realce_linear_rgb(pixels):

    #separa os canais R, G e B
    canal_r = pixels[0::3]   # pega de 3 em 3, começando no índice 0
    canal_g = pixels[1::3]   # pega de 3 em 3, começando no índice 1
    canal_b = pixels[2::3]   # pega de 3 em 3, começando no índice 2

    print("\n--- Canal Vermelho (R) ---")
    canal_r_saida = realce_linear(canal_r)

    print("\n--- Canal Verde (G) ---")
    canal_g_saida = realce_linear(canal_g)

    print("\n--- Canal Azul (B) ---")
    canal_b_saida = realce_linear(canal_b)

    pixels_saida = []

    for i in range(len(canal_r_saida)):
        pixels_saida.append(canal_r_saida[i])
        pixels_saida.append(canal_g_saida[i])
        pixels_saida.append(canal_b_saida[i])

    return pixels_saida


#calcular histograma (256 níveis)
def calcular_histograma(pixels):

    histograma = [0] * 256

    for pixel in pixels:
        histograma[pixel] += 1

    return histograma


#gerar grafico do histograma RGB
#mostra os 3 canais sobrepostos (R, G, B)
def gerar_grafico_histograma_rgb(histograma_r, histograma_g, histograma_b, titulo, nome_arquivo):

    # valores de 0 até 255
    niveis = []

    for i in range(256):
        niveis.append(i)

    plt.figure(figsize=(10, 5))

    #cada canal com sua cor e transparência para sobreposição
    plt.bar(niveis, histograma_r, width=1, color='red',   alpha=0.5, label='Vermelho (R)')
    plt.bar(niveis, histograma_g, width=1, color='green', alpha=0.5, label='Verde (G)')
    plt.bar(niveis, histograma_b, width=1, color='blue',  alpha=0.5, label='Azul (B)')

    plt.title(titulo)
    plt.xlabel("Nível de intensidade")
    plt.ylabel("Quantidade de pixels")

    plt.xlim(0, 255)
    plt.legend()

    plt.savefig(nome_arquivo)

    plt.show()


# PROGRAMA PRINCIPAL ----------------------------------------

pasta_programa = os.path.dirname(os.path.abspath(__file__))
pasta_img = os.path.join(pasta_programa, "ImgPpm")

arquivo_entrada = os.path.join(
    pasta_img,
    "Entrada_RGB.ppm"
)

arquivo_saida = os.path.join(
    pasta_img,
    "Saida_RGB.ppm"
)

resultado = ler_ppm(arquivo_entrada)

if resultado is not None:

    largura, altura, valor_maximo, pixels = resultado

    print("----------------------------------")
    print("Imagem PPM (RGB)")
    print("----------------------------------")
    print("Largura:", largura)
    print("Altura:", altura)
    print("Valor máximo:", valor_maximo)
    print("Quantidade de valores:", len(pixels))
    print("Quantidade de pixels (R+G+B):", len(pixels) // 3)

    #histograma da imagem original (RGB)
    canal_r_orig = pixels[0::3]
    canal_g_orig = pixels[1::3]
    canal_b_orig = pixels[2::3]

    histograma_r_orig = calcular_histograma(canal_r_orig)
    histograma_g_orig = calcular_histograma(canal_g_orig)
    histograma_b_orig = calcular_histograma(canal_b_orig)

    gerar_grafico_histograma_rgb(
        histograma_r_orig,
        histograma_g_orig,
        histograma_b_orig,
        "Histograma RGB - Imagem Original",
        os.path.join(pasta_img, "Histograma_Original.png")
    )

    #realce linear RGB
    pixels_saida = realce_linear_rgb(pixels)

    salvar_ppm(
        arquivo_saida,
        largura,
        altura,
        255,
        pixels_saida
    )

    print("----------------------------------")
    print("Imagem realçada salva em:")
    print(arquivo_saida)

    #histograma da imagem realcada(RGB)
    canal_r_saida = pixels_saida[0::3]
    canal_g_saida = pixels_saida[1::3]
    canal_b_saida = pixels_saida[2::3]

    histograma_r_saida = calcular_histograma(canal_r_saida)
    histograma_g_saida = calcular_histograma(canal_g_saida)
    histograma_b_saida = calcular_histograma(canal_b_saida)

    gerar_grafico_histograma_rgb(
        histograma_r_saida,
        histograma_g_saida,
        histograma_b_saida,
        "Histograma RGB - Imagem Realçada",
        os.path.join(pasta_img, "Histograma_Realce.png")
    )

    print("----------------------------------")
    print("Processamento concluído!")