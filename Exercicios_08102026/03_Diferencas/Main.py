import sys
from pathlib import Path
from time import perf_counter


PASTA_ATUAL = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_ATUAL.parent

# Permite importar as classes compartilhadas da pasta principal.
sys.path.insert(0, str(PASTA_PROJETO))

from Imagem import Imagem
from CompressaoMelhorada import CompressaoMelhorada


MODO = "diferencas"


def processar(entrada, pasta_saida):
    imagem = Imagem.ler(entrada)

    inicio = perf_counter()
    comprimido = CompressaoMelhorada.comprimir(imagem, MODO)
    tempo_compressao = perf_counter() - inicio

    arquivo_rle = pasta_saida / f"{entrada.name}.rle"

    #repetir a execução substitui a saída
    arquivo_rle.write_bytes(comprimido)

    #recupera os dados do arquivo salvo
    conteudo_salvo = arquivo_rle.read_bytes()

    inicio = perf_counter()
    restaurada = CompressaoMelhorada.descomprimir(conteudo_salvo)
    tempo_descompressao = perf_counter() - inicio

    original = (
        imagem.largura, imagem.altura,
        imagem.maximo, imagem.canais, imagem.pixels
    )

    recuperada = (
        restaurada.largura, restaurada.altura,
        restaurada.maximo, restaurada.canais, restaurada.pixels
    )

    if original != recuperada:
        raise ValueError("A reconstrução alterou a imagem.")

    arquivo_restaurado = pasta_saida / (
        f"{entrada.stem}_restaurada{entrada.suffix}"
    )

    restaurada.salvar(arquivo_restaurado)

    print(f"\nImagem: {entrada.name}")

    for linha in comprimido.split(b"\n", 5)[:5]:
        print(linha.decode("ascii"))

    print(f"Entrada: {imagem.tamanho_original} bytes")
    print(f"Comprimido: {len(comprimido)} bytes")
    print(f"Compressão: {tempo_compressao:.4f} segundos")
    print(f"Descompressão: {tempo_descompressao:.4f} segundos")
    print("Reconstrução exata: OK")


def main():
    pasta_entrada = PASTA_PROJETO / "Img" / "Entrada"
    pasta_saida = PASTA_ATUAL / "Img" / "Saida"

    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivos = [
        "Mandelbrot_Cinza.pgm",
        "Barras_RGB.ppm"
    ]

    for nome in arquivos:
        processar(pasta_entrada / nome, pasta_saida)


if __name__ == "__main__":
    main()