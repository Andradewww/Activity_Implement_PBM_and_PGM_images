import os

from LeitorTiff import ler_tiff

from Equalizacao import (
    calcular_histograma,
    calcular_probabilidade,
    calcular_acumulado,
    calcular_transformacao,
    equalizar,
    gerar_histograma
)

#pasta das imagens
pasta = os.path.join(
    os.path.dirname(__file__),
    "ImgEqualizacao"
)

imagens = [

    "Fig0316(1)(top_left).tif",

    "Fig0316(2)(2nd_from_top).tif",

    "Fig0316(3)(third_from_top).tif",

    "Fig0316(4)(bottom_left).tif"

]

#processamento
for numero, nome in enumerate(imagens,start=1):

    print()
    print("Processando:", nome)
    print("--------------------------------")

    caminho = os.path.join(pasta, nome)

    resultado = ler_tiff(caminho)

    if resultado is None:

        print("Não foi possível ler a imagem.")

        continue

    largura, altura, pixels = resultado

    print("Largura:",largura)
    print("Altura:",altura)
    print("Pixels:",len(pixels))


    #histograma original
    histograma = calcular_histograma(pixels)

    gerar_histograma(

        histograma,

        "Histograma Original " + str(numero),

        os.path.join(pasta, "Histograma_Original_" + str(numero) + ".png")
    )

    #calc. probabilidade
    probabilidades = (
        calcular_probabilidade(histograma, len(pixels))
    )

    #calc. acumulado
    acumulado = (
        calcular_acumulado(probabilidades)
    )

    #calc. transformacao
    transformacao = (
        calcular_transformacao(acumulado)
    )

    #equalizacao
    pixels_saida = equalizar(pixels, transformacao)

    #salvar PGM
    nome_saida = ("Saida_Equalizada_" + str(numero) + ".pgm")

    caminho_saida = os.path.join(pasta, nome_saida)

    arquivo = open(caminho_saida, "w")

    arquivo.write("P2\n")

    arquivo.write(str(largura) + " " + str(altura) + "\n")

    arquivo.write("255\n")

    contador = 0

    for pixel in pixels_saida:

        arquivo.write(str(pixel) + " ")

        contador += 1

        if contador == largura:

            arquivo.write("\n")

            contador = 0

    arquivo.close()

    #histograma equalizado
    histograma_saida = (
        calcular_histograma(pixels_saida)
    )

    gerar_histograma(

        histograma_saida,

        "Histograma Equalizado "
        + str(numero),

        os.path.join(pasta,"Histograma_Equalizado_" + str(numero) + ".png")
    )

    print("Imagem salva:", caminho_saida)


print()
print("--------------------------------")
print("PROCESSAMENTO CONCLUÍDO")
