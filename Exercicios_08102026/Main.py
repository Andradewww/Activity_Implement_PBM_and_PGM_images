from pathlib import Path

from Imagem import Imagem
from CompressaoPorRepeticao import CompressaoPorRepeticao


def processar(entrada, pasta_saida):
    imagem = Imagem.ler(entrada)
    comprimido = CompressaoPorRepeticao.comprimir(imagem)
    restaurada = CompressaoPorRepeticao.descomprimir(comprimido)

    #verifica dimensoes, canais e todos os pixels
    original = (
        imagem.largura, imagem.altura,
        imagem.maximo, imagem.canais, imagem.pixels
    )

    recuperada = (
        restaurada.largura, restaurada.altura,
        restaurada.maximo, restaurada.canais, restaurada.pixels
    )

    if original != recuperada:
        raise ValueError("A imagem reconstruída é diferente da original.")

    arquivo_rle = pasta_saida / f"{entrada.name}.rle"
    arquivo_restaurado = pasta_saida / (
        f"{entrada.stem}_restaurada{entrada.suffix}"
    )

    #não sobrescreve uma saída existente.
    with arquivo_rle.open("xb") as arquivo:
        arquivo.write(comprimido)

    restaurada.salvar(arquivo_restaurado)

    cabecalho = comprimido.split(b"\n", 5)[:5]

    print(f"\nImagem: {entrada.name}")

    for linha in cabecalho:
        print(linha.decode("ascii"))

    print("Reconstrução exata: OK")


def main():
    pasta = Path(__file__).resolve().parent
    pasta_entrada = pasta / "Img" / "Entrada"
    pasta_saida = pasta / "Img" / "Saida"

    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivos = [
        "Mandelbrot_Cinza.pgm",
        "Barras_RGB.ppm"
    ]

    for nome in arquivos:
        processar(pasta_entrada / nome, pasta_saida)


if __name__ == "__main__":
    main()