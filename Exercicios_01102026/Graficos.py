import matplotlib.pyplot as plt


def gerar_grafico_histograma(histograma, titulo, nome_arquivo):

    niveis = []

    for i in range(256):
        niveis.append(i)

    plt.figure()

    plt.bar(niveis, histograma, width=1)

    plt.title(titulo)

    plt.xlabel("Nível de intensidade")

    plt.ylabel("Quantidade de pixels")

    plt.xlim(0, 255)

    plt.savefig(nome_arquivo)

    plt.show()
    plt.close()