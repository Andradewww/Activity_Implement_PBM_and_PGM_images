def calcular_histograma(pixels):

    #256 niveis de intensidade
    histograma = [0] * 256

    for pixel in pixels:
        histograma[pixel] += 1

    return histograma