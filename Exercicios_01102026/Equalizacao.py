import matplotlib.pyplot as plt

#histograma
def calcular_histograma(pixels):

    histograma = [0] * 256

    for pixel in pixels:

        histograma[pixel] += 1

    return histograma


#probabilidade
def calcular_probabilidade(histograma, total_pixels):

    probabilidades = []

    for quantidade in histograma:

        probabilidades.append(quantidade / total_pixels)

    return probabilidades


#probabilidade acumulada
def calcular_acumulado(probabilidades):

    acumulado = []

    soma = 0

    for valor in probabilidades:

        soma += valor
        acumulado.append(soma)

    return acumulado


#funcao transformacao
def calcular_transformacao(acumulado):

    transformacao = []

    for valor in acumulado:

        novo_valor = (255 * valor)
        novo_valor = int(round(novo_valor))
        transformacao.append(novo_valor)

    return transformacao


#equalizar imagem
def equalizar(pixels, transformacao):

    pixels_saida = []

    for pixel in pixels:
        pixels_saida.append(
            transformacao[pixel]
        )

    return pixels_saida


#grafico
def gerar_histograma(histograma,titulo,arquivo_saida):

    niveis = range(256)
    plt.figure()

    plt.bar(niveis,histograma,width=1)

    plt.title(titulo)

    plt.xlabel("Nível de intensidade")

    plt.ylabel("Quantidade de pixels")

    plt.xlim(0, 255)

    plt.savefig(arquivo_saida)

    plt.show()
    plt.close()