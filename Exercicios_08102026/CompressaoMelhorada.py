from Imagem import Imagem
from CompressaoPorRepeticao import CompressaoPorRepeticao


class CompressaoMelhorada:

    @staticmethod
    def codificar(imagem, direcao, usar_diferencas):
        dados = bytearray()

        if direcao == "L":
            quantidade = imagem.altura
            comprimento = imagem.largura
        else:
            quantidade = imagem.largura
            comprimento = imagem.altura

        for posicao in range(quantidade):
            for canal in range(imagem.canais):
                valores = []

                for indice in range(comprimento):
                    if direcao == "L":
                        valor = imagem.pixels[posicao][indice][canal]
                    else:
                        valor = imagem.pixels[indice][posicao][canal]

                    valores.append(valor)

                if usar_diferencas:
                    diferencas = []
                    anterior = 0

                    for atual in valores:
                        diferencas.append((atual - anterior) % 256)
                        anterior = atual

                    valores = diferencas

                bloco = CompressaoPorRepeticao.comprimir_sequencia(
                    valores
                )

                dados.extend(bloco)

        return dados

    @staticmethod
    def criar_cabecalho(imagem, direcao, transformacao, tamanho):
        tamanho_pixels = (
            imagem.largura * imagem.altura * imagem.canais
        )

        reducao_arquivo = (
            1 - tamanho / imagem.tamanho_original
        ) * 100

        reducao_pixels = (
            1 - tamanho / tamanho_pixels
        ) * 100

        texto = (
            "RLE2\n"
            f"{imagem.largura} {imagem.altura} "
            f"{imagem.maximo} {imagem.canais} "
            f"{direcao} {transformacao}\n"
            f"BYTES_ORIGINAL {imagem.tamanho_original}\n"
            f"REDUCAO_ARQUIVO_PCT {reducao_arquivo:+020.6f}\n"
            f"REDUCAO_PIXELS_PCT {reducao_pixels:+020.6f}\n"
        )

        return texto.encode("ascii")

    @staticmethod
    def comprimir(imagem, modo):
        if modo == "direcao":
            linhas = CompressaoMelhorada.codificar(
                imagem, "L", False
            )

            colunas = CompressaoMelhorada.codificar(
                imagem, "C", False
            )

            #em caso de empate, mantém a leitura por linhas.
            if len(linhas) <= len(colunas):
                dados = linhas
                direcao = "L"
            else:
                dados = colunas
                direcao = "C"

            transformacao = "N"

        elif modo == "diferencas":
            dados = CompressaoMelhorada.codificar(
                imagem, "L", True
            )

            direcao = "L"
            transformacao = "D"

        else:
            raise ValueError("Modo de compressão desconhecido.")

        #calcula o tamanho incluindo o cabecalho
        inicial = CompressaoMelhorada.criar_cabecalho(
            imagem, direcao, transformacao, 0
        )

        tamanho_total = len(inicial) + len(dados)

        cabecalho = CompressaoMelhorada.criar_cabecalho(
            imagem, direcao, transformacao, tamanho_total
        )

        if len(cabecalho) != len(inicial):
            raise ValueError("Taxa excedeu o espaço do cabeçalho.")

        return cabecalho + dados

    @staticmethod
    def descomprimir(conteudo):
        partes = conteudo.split(b"\n", 5)

        if len(partes) != 6 or partes[0] != b"RLE2":
            raise ValueError("Arquivo de compressão inválido.")

        campos = partes[1].split()

        if len(campos) != 6:
            raise ValueError("Cabeçalho inválido.")

        largura, altura, maximo, canais = map(int, campos[:4])
        direcao = campos[4].decode("ascii")
        transformacao = campos[5].decode("ascii")

        if (
            largura <= 0
            or altura <= 0
            or canais not in (1, 3)
            or not 1 <= maximo <= 255
            or direcao not in ("L", "C")
            or transformacao not in ("N", "D")
        ):
            raise ValueError("Informações da imagem inválidas.")

        pixels = [
            [[0] * canais for _ in range(largura)]
            for _ in range(altura)
        ]

        if direcao == "L":
            quantidade = altura
            comprimento = largura
        else:
            quantidade = largura
            comprimento = altura

        dados = partes[5]
        indice = 0

        for posicao in range(quantidade):
            for canal in range(canais):
                #diferencas podem ocupar todo o intervalo 0–255
                limite = 255 if transformacao == "D" else maximo

                valores, indice = (
                    CompressaoPorRepeticao.descomprimir_sequencia(
                        dados, indice, comprimento, limite
                    )
                )

                if transformacao == "D":
                    anterior = 0

                    for i, diferenca in enumerate(valores):
                        atual = (anterior + diferenca) % 256
                        valores[i] = atual
                        anterior = atual

                if any(valor > maximo for valor in valores):
                    raise ValueError("Pixel reconstruído inválido.")

                for i, valor in enumerate(valores):
                    if direcao == "L":
                        pixels[posicao][i][canal] = valor
                    else:
                        pixels[i][posicao][canal] = valor

        if indice != len(dados):
            raise ValueError("Dados excedentes no arquivo.")

        return Imagem(largura, altura, maximo, canais, pixels)