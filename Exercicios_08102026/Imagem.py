from pathlib import Path


class Imagem:
    def __init__(self, largura, altura, maximo, canais, pixels):
        self.largura = largura
        self.altura = altura
        self.maximo = maximo
        self.canais = canais
        self.pixels = pixels
        self.tamanho_original = 0

    @classmethod
    def ler(cls, caminho):
        conteudo = Path(caminho).read_bytes()
        posicao = 0
        espacos = b" \t\r\n\v\f"

        #le uma informacao do cabeçalho
        def proximo_token():
            nonlocal posicao

            while posicao < len(conteudo):
                caractere = conteudo[posicao]

                if caractere in espacos:
                    posicao += 1

                elif caractere == ord("#"):
                    #ignora o comentario ate o final da linha
                    while (
                        posicao < len(conteudo)
                        and conteudo[posicao] not in b"\r\n"
                    ):
                        posicao += 1

                else:
                    break

            inicio = posicao

            while (
                posicao < len(conteudo)
                and conteudo[posicao] not in espacos
                and conteudo[posicao] != ord("#")
            ):
                posicao += 1

            if inicio == posicao:
                raise ValueError("Cabeçalho incompleto.")

            return conteudo[inicio:posicao]

        formato = proximo_token()

        if formato not in (b"P2", b"P3", b"P5", b"P6"):
            raise ValueError("Use uma imagem PGM ou PPM.")

        largura = int(proximo_token())
        altura = int(proximo_token())
        maximo = int(proximo_token())

        canais = 1 if formato in (b"P2", b"P5") else 3

        if largura <= 0 or altura <= 0:
            raise ValueError("Dimensões inválidas.")

        if not 1 <= maximo <= 255:
            raise ValueError("Esta implementação aceita até 8 bits.")

        if formato in (b"P2", b"P3"):
            # Formatos em texto: números separados por espaços.
            dados = []

            for linha in conteudo[posicao:].splitlines():
                linha = linha.split(b"#", 1)[0]
                dados.extend(linha.split())

            valores = list(map(int, dados))

        else:
            #formatos binarios: um byte por intensidade
            if (
                posicao >= len(conteudo)
                or conteudo[posicao] not in espacos
            ):
                raise ValueError("Separador do cabeçalho ausente.")

            #consome o separador, também aceita quebra CRLF
            if conteudo[posicao:posicao + 2] == b"\r\n":
                posicao += 2
            else:
                posicao += 1

            valores = conteudo[posicao:]

        quantidade_esperada = largura * altura * canais

        if len(valores) != quantidade_esperada:
            raise ValueError("Quantidade incorreta de valores.")

        if any(valor < 0 or valor > maximo for valor in valores):
            raise ValueError("Intensidade inválida.")

        pixels = []
        indice = 0

        for _ in range(altura):
            linha = []

            for _ in range(largura):
                pixel = list(valores[indice:indice + canais])
                linha.append(pixel)
                indice += canais

            pixels.append(linha)

        imagem = cls(largura, altura, maximo, canais, pixels)
        imagem.tamanho_original = len(conteudo)

        return imagem

    def salvar(self, caminho):
        formato = "P2" if self.canais == 1 else "P3"

        linhas = [
            formato,
            f"{self.largura} {self.altura}",
            str(self.maximo)
        ]

        for linha in self.pixels:
            valores = []

            for pixel in linha:
                valores.extend(str(valor) for valor in pixel)

            linhas.append(" ".join(valores))

        texto = "\n".join(linhas) + "\n"

        #evita sobrescrever um arquivo existente
        with Path(caminho).open("w", encoding="ascii", newline="\n") as arquivo:
            arquivo.write(texto)