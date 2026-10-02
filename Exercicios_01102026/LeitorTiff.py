import struct

def ler_tiff(nome_arquivo):

    arquivo = open(nome_arquivo, "rb")

    #ordem dos bytes
    ordem = arquivo.read(2)

    if ordem == b"II":
        endian = "<"

    elif ordem == b"MM":
        endian = ">"

    else:
        print("Arquivo TIFF inválido.")
        arquivo.close()
        return None

    #identificador TIFF
    identificador = struct.unpack(endian + "H", arquivo.read(2))[0]

    if identificador != 42:
        print("Identificador TIFF inválido.")
        arquivo.close()
        return None

    #localização da IFD
    offset = struct.unpack(endian + "I", arquivo.read(4))[0]

    arquivo.seek(offset)

    quantidade = struct.unpack(endian + "H", arquivo.read(2))[0]

    largura = 0
    altura = 0
    bits = 0
    compressao = 0
    amostras = 1

    offsets = []
    tamanhos = []

    #ler as informações do TIFF
    for i in range(quantidade):

        tag = struct.unpack(endian + "H", arquivo.read(2))[0]

        tipo = struct.unpack(endian + "H", arquivo.read(2))[0]

        quantidade_valores = struct.unpack(endian + "I", arquivo.read(4))[0]

        campo = arquivo.read(4)


        if tipo == 3:

            tamanho = 2

            if quantidade_valores == 1:

                valores = [struct.unpack(endian + "H", campo[:2])[0]]

            else:

                posicao = arquivo.tell()

                local = struct.unpack(endian + "I", campo)[0]

                arquivo.seek(local)

                valores = []

                for j in range(quantidade_valores):

                    valores.append(
                        struct.unpack(endian + "H", arquivo.read(2))[0]
                    )

                arquivo.seek(posicao)

        #long
        elif tipo == 4:

            tamanho = 4

            if quantidade_valores == 1:

                valores = [struct.unpack(endian + "I", campo)[0]]
            else:

                posicao = arquivo.tell()

                local = struct.unpack(endian + "I", campo)[0]

                arquivo.seek(local)

                valores = []

                for j in range(quantidade_valores):

                    valores.append(
                        struct.unpack(endian + "I", arquivo.read(4))[0]
                    )

                arquivo.seek(posicao)

        else:

            valores = []

        #tags

        if tag == 256:
            largura = valores[0]

        elif tag == 257:
            altura = valores[0]

        elif tag == 258:
            bits = valores[0]

        elif tag == 259:
            compressao = valores[0]

        elif tag == 273:
            offsets = valores

        elif tag == 277:
            amostras = valores[0]

        elif tag == 279:
            tamanhos = valores

    arquivo.close()

    #verificações
    if bits != 8:
        print("A imagem não possui 8 bits.")

        return None

    if compressao != 1:
        print("A imagem está comprimida.")

        return None

    if amostras != 1:
        print("A imagem não está em escala de cinza.")

        return None

    if len(offsets) == 0:
        print("Dados da imagem não encontrados.")

        return None

    #ler pixels
    arquivo = open(nome_arquivo,"rb")

    pixels = []

    for i in range(len(offsets)):

        arquivo.seek(offsets[i])

        dados = arquivo.read(tamanhos[i])

        for valor in dados:
            pixels.append(valor)

    arquivo.close()

    #garantir quantidade correta
    quantidade_pixels = (largura * altura)

    pixels = pixels[
        :quantidade_pixels
    ]

    return largura, altura, pixels