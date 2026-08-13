import os
import random

SAIDA = r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade01\Imagens"

RESOLUCOES = {
    "100x100": (100, 100),
    "HD":      (1280, 720),
    "FullHD":  (1920, 1080),
    "4K":      (3840, 2160),
    "8K":      (7680, 4320),
}

os.makedirs(SAIDA, exist_ok=True)

for nome, (larg, alt) in RESOLUCOES.items():
    # PBM - Tipo P1 (pixels 0/1, máx. 70 caracteres por linha)
    with open(os.path.join(SAIDA, f"aleatoria_{nome}.pbm"), "w") as f:
        f.write(f"P1\n{larg} {alt}\n")
        for _ in range(alt):
            bits = format(random.getrandbits(larg), f"0{larg}b")
            for i in range(0, larg, 35):
                f.write(" ".join(bits[i:i + 35]) + "\n")

    # PGM - Tipo P2 (16 níveis de cinza, maxval 15, máx. 70 caracteres por linha)
    with open(os.path.join(SAIDA, f"aleatoria_{nome}.pgm"), "w") as f:
        f.write(f"P2\n{larg} {alt}\n15\n")
        for _ in range(alt):
            linha = random.choices(range(16), k=larg)
            for i in range(0, larg, 23):
                f.write(" ".join(map(str, linha[i:i + 23])) + "\n")

    print(f"{nome} ok")