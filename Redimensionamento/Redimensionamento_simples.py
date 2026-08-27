import os

ENTRADA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Redimensionamento\Entrada_EscalaCinza.pgm"

SAIDA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Redimensionamento\Imagens\simples"

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


#redimensiona usando vizinho mais proximo
def redimensionar(imagem, nova_largura, nova_altura):

    altura = len(imagem)
    largura = len(imagem[0])

    nova_imagem = []

    for y in range(nova_altura):

        linha = []

        origem_y = int(y * altura / nova_altura)

        for x in range(nova_largura):

            origem_x = int(x * largura / nova_largura)

            linha.append(imagem[origem_y][origem_x])

        nova_imagem.append(linha)

    return nova_imagem


#leitura da imagem original
imagem, largura, altura, maxval = ler_pgm(ENTRADA)

print(f"Imagem original: {largura}x{altura}")


#a)10x menor
nova_largura = largura // 10
nova_altura = altura // 10

imagem_nova = redimensionar(imagem, nova_largura, nova_altura)

salvar_pgm(
    os.path.join(SAIDA, "01_10x_menor.pgm"),
    imagem_nova,
    nova_largura,
    nova_altura,
    maxval
)


#b)480x320
imagem_nova = redimensionar(imagem, 480, 320)

salvar_pgm(
    os.path.join(SAIDA, "02_480x320.pgm"),
    imagem_nova,
    480,
    320,
    maxval
)


#c)720p HD
imagem_nova = redimensionar(imagem, 1280, 720)

salvar_pgm(
    os.path.join(SAIDA, "03_720p_HD.pgm"),
    imagem_nova,
    1280,
    720,
    maxval
)


#d)1080p Full HD
imagem_nova = redimensionar(imagem, 1920, 1080)

salvar_pgm(
    os.path.join(SAIDA, "04_1080p_FullHD.pgm"),
    imagem_nova,
    1920,
    1080,
    maxval
)


#e)4K
imagem_nova = redimensionar(imagem, 3840, 2160)

salvar_pgm(
    os.path.join(SAIDA, "05_4K.pgm"),
    imagem_nova,
    3840,
    2160,
    maxval
)


#e)8K
imagem_nova = redimensionar(imagem, 7680, 4320)

salvar_pgm(
    os.path.join(SAIDA, "06_8K.pgm"),
    imagem_nova,
    7680,
    4320,
    maxval
)


print("Imagens geradas!")