from Imagem import Imagem


class CompressaoPorRepeticao:
    LIMITE = 127

    @staticmethod
    def comprimir_sequencia(valores):
        resultado = bytearray()
        indice = 0

        while indice < len(valores):
            quantidade = 1

            #conta valores iguais consecutivos
            while (
                quantidade < CompressaoPorRepeticao.LIMITE
                and indice + quantidade < len(valores)
                and valores[indice] == valores[indice + quantidade]
            ):
                quantidade += 1

            if quantidade >= 2:
                resultado.extend([quantidade, valores[indice]])
                indice += quantidade

            else:
                inicio = indice
                indice += 1

                #agrupa valores sem repetição consecutiva
                while (
                    indice < len(valores)
                    and indice - inicio < CompressaoPorRepeticao.LIMITE
                ):
                    if (
                        indice + 1 < len(valores)
                        and valores[indice] == valores[indice + 1]
                    ):
                        break

                    indice += 1

                quantidade = indice - inicio

                #converte o contador negativo para um byte
                resultado.append((-quantidade) & 255)
                resultado.extend(valores[inicio:indice])

        return resultado

    @staticmethod
    def criar_cabecalho(imagem, tamanho_total):
        tamanho_pixels = (
            imagem.largura * imagem.altura * imagem.canais
        )

        reducao_arquivo = (
            1 - tamanho_total / imagem.tamanho_original
        ) * 100

        reducao_pixels = (
            1 - tamanho_total / tamanho_pixels
        ) * 100

        #as taxas ocupam campos de tamanho fixo
        texto = (
            "RLE1\n"
            f"{imagem.largura} {imagem.altura} "
            f"{imagem.maximo} {imagem.canais}\n"
            f"BYTES_ORIGINAL {imagem.tamanho_original}\n"
            f"REDUCAO_ARQUIVO_PCT {reducao_arquivo:+020.6f}\n"
            f"REDUCAO_PIXELS_PCT {reducao_pixels:+020.6f}\n"
        )

        return texto.encode("ascii")

    @staticmethod
    def comprimir(imagem):
        dados = bytearray()

        for linha in imagem.pixels:
            #cinza: um canal RGB: R, G e B, nessa ordem
            for canal in range(imagem.canais):
                valores = [pixel[canal] for pixel in linha]
                dados.extend(CompressaoPorRepeticao.comprimir_sequencia(valores))

        #calcula o tamanho completo, incluindo o cabecalho
        cabecalho_inicial = CompressaoPorRepeticao.criar_cabecalho(imagem, 0)
        tamanho_total = len(cabecalho_inicial) + len(dados)

        cabecalho = CompressaoPorRepeticao.criar_cabecalho(imagem, tamanho_total)

        if len(cabecalho) != len(cabecalho_inicial):
            raise ValueError("Taxa excedeu o espaço do cabeçalho.")

        return cabecalho + dados

    @staticmethod
    def descomprimir_sequencia(dados, indice, largura, maximo):
        valores = []

        while len(valores) < largura:
            if indice >= len(dados):
                raise ValueError("Arquivo RLE incompleto.")

            contador = dados[indice]
            indice += 1

            #interpreta somente o contador como valor com sinal
            if contador >= 128:
                contador -= 256

            if contador in (0, -128):
                raise ValueError("Contador inválido.")

            quantidade = abs(contador)

            if len(valores) + quantidade > largura:
                raise ValueError("Bloco ultrapassa a largura da linha.")

            if contador > 0:
                if indice >= len(dados):
                    raise ValueError("Valor repetido ausente.")

                bloco = [dados[indice]] * quantidade
                indice += 1

            else:
                if indice + quantidade > len(dados):
                    raise ValueError("Bloco literal incompleto.")

                bloco = list(dados[indice:indice + quantidade])
                indice += quantidade

            if any(valor > maximo for valor in bloco):
                raise ValueError("Intensidade inválida.")

            valores.extend(bloco)

        return valores, indice

    @staticmethod
    def descomprimir(conteudo):
        #cabecalho contém cinco linhas.
        partes = conteudo.split(b"\n", 5)

        if len(partes) != 6 or partes[0] != b"RLE1":
            raise ValueError("Cabeçalho RLE inválido.")

        largura, altura, maximo, canais = map(
            int, partes[1].split()
        )

        if (
            largura <= 0
            or altura <= 0
            or canais not in (1, 3)
            or not 1 <= maximo <= 255
        ):
            raise ValueError("Dados da imagem inválidos.")

        dados = partes[5]
        pixels = []
        indice = 0

        for _ in range(altura):
            linha = [[0] * canais for _ in range(largura)]

            for canal in range(canais):
                valores, indice = CompressaoPorRepeticao.descomprimir_sequencia(
                    dados, indice, largura, maximo
                )

                for coluna, valor in enumerate(valores):
                    linha[coluna][canal] = valor

            pixels.append(linha)

        if indice != len(dados):
            raise ValueError("Dados excedentes no arquivo RLE.")

        return Imagem(largura, altura, maximo, canais, pixels)