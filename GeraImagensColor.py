import os
import random

SAIDA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\ImagensColoridas"

RESOLUCOES = {
    "100x100": (100, 100, 15),       #16 intensidades: 0 a 15
    "1000x1000": (1000, 1000, 255),  #256 intensidades: 0 a 255
    "4K": (3840, 2160, 255),         #256 intensidades: 0 a 255
}

os.makedirs(SAIDA, exist_ok=True)

for nome, (larg, alt, maxval) in RESOLUCOES.items():

    #PPM - Tipo P3 (ASCII)
    with open(os.path.join(SAIDA, f"aleatoria_{nome}.ppm"), "w") as f:

        #cabecalho do arquivo PPM
        f.write(f"P3\n{larg} {alt}\n{maxval}\n")

        #geracao dos pixels RGB
        linha = ""

        for _ in range(alt):
            for _ in range(larg):

                #valores aleatórios para R, G e B
                r = random.randint(0, maxval)
                g = random.randint(0, maxval)
                b = random.randint(0, maxval)

                pixel = f"{r} {g} {b} "

                #mantem o limite de ~70 caracteres por linha
                if len(linha) + len(pixel) > 69:
                    f.write(linha.rstrip() + "\n")
                    linha = ""

                linha += pixel

        #escreve os valores restantes
        if linha:
            f.write(linha.rstrip() + "\n")

    print(f"{nome} ok")