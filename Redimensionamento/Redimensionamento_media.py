import os
import math

ENTRADA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Redimensionamento\Entrada_EscalaCinza.pgm"
SAIDA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Redimensionamento\Imagens\media"

os.makedirs(SAIDA, exist_ok=True)


#leitura da imagem PGM
def ler_pgm(caminho):
    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()

    largura, altura = map(int, linhas[1].split())
    maxval = int(linhas[2])

    valores = []
    for linha in linhas[3:]:
        valores.extend(map(int, linha.split()))

    imagem = []
    posicao = 0

    for y in range(altura):
        linha = []

        for x in range(largura):
            linha.append(valores[posicao])
            posicao += 1

        imagem.append(linha)

    return imagem, largura, altura, maxval


#salva a imagem PGM
def salvar_pgm(caminho, imagem, largura, altura, maxval):
    with open(caminho, "w") as arquivo:
        arquivo.write("P2\n")
        arquivo.write(f"{largura} {altura}\n")
        arquivo.write(f"{maxval}\n")

        for linha in imagem:
            arquivo.write(" ".join(map(str, linha)) + "\n")


#reducao usando media
def reduzir_media(imagem, nova_largura, nova_altura):

    altura = len(imagem)
    largura = len(imagem[0])

    nova_imagem = []

    for y in range(nova_altura):
        linha = []

        y_inicio = int(y * altura / nova_altura)
        y_fim = int((y + 1) * altura / nova_altura)

        for x in range(nova_largura):

            x_inicio = int(x * largura / nova_largura)
            x_fim = int((x + 1) * largura / nova_largura)

            soma = 0
            quantidade = 0

            for yy in range(y_inicio, y_fim):
                for xx in range(x_inicio, x_fim):
                    soma += imagem[yy][xx]
                    quantidade += 1

            linha.append(round(soma / quantidade))

        nova_imagem.append(linha)

    return nova_imagem


#interpolacao bilinear
def interpolar(imagem, nova_largura, nova_altura):

    altura = len(imagem)
    largura = len(imagem[0])

    nova_imagem = []

    for y in range(nova_altura):

        linha = []

        origem_y = y * (altura - 1) / (nova_altura - 1)

        y1 = int(math.floor(origem_y))
        y2 = min(y1 + 1, altura - 1)
        dy = origem_y - y1

        for x in range(nova_largura):

            origem_x = x * (largura - 1) / (nova_largura - 1)

            x1 = int(math.floor(origem_x))
            x2 = min(x1 + 1, largura - 1)
            dx = origem_x - x1

            p1 = imagem[y1][x1]
            p2 = imagem[y1][x2]
            p3 = imagem[y2][x1]
            p4 = imagem[y2][x2]

            valor = (
                p1 * (1 - dx) * (1 - dy) +
                p2 * dx * (1 - dy) +
                p3 * (1 - dx) * dy +
                p4 * dx * dy
            )

            linha.append(round(valor))

        nova_imagem.append(linha)

    return nova_imagem


#leitura da imagem original
imagem, largura, altura, maxval = ler_pgm(ENTRADA)

print(f"Imagem original: {largura}x{altura}")


#a) 10x menor usando média
largura_10 = largura // 10
altura_10 = altura // 10

imagem_10 = reduzir_media(imagem, largura_10, altura_10)

salvar_pgm(
    os.path.join(SAIDA, "01_10x_menor_media.pgm"),
    imagem_10,
    largura_10,
    altura_10,
    maxval
)


#b, c, d, e - redimensionamentos interpolados
resolucoes = {
    "02_480x320": (480, 320),
    "03_720p_HD": (1280, 720),
    "04_1080p_FullHD": (1920, 1080),
    "05_4K": (3840, 2160),
    "06_8K": (7680, 4320)
}

for nome, (nova_largura, nova_altura) in resolucoes.items():

    imagem_nova = interpolar(
        imagem,
        nova_largura,
        nova_altura
    )

    salvar_pgm(
        os.path.join(SAIDA, nome + "_interpolada.pgm"),
        imagem_nova,
        nova_largura,
        nova_altura,
        maxval
    )

    print(nome, "concluído")

print("Atividade concluída!")