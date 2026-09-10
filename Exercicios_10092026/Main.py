import csv
import matplotlib.pyplot as plt


#funcao para ler imagem PGM P2
def ler_pgm(nome_arquivo):
    
    arquivo = open(nome_arquivo, "r")
    
    #le todas as linhas
    linhas = arquivo.readlines()
    
    arquivo.close()
    
    #remove comentarios e linhas vazias
    dados = []
    
    for linha in linhas:
        linha = linha.strip()
        
        if linha != "" and not linha.startswith("#"):
            dados.extend(linha.split())
            
    #primeiro valor P2
    formato = dados[0]
    
    if formato != "P2":
        print("Erro - o arquivo não é PGM P2")
        return None
    
    largura = int(dados[1])
    altura = int(dados[2])
    valor_maximo = int(dados[3])
    
    #pixels começam na posicao 4
    pixels = []
    
    for i in range(4, len(dados)):
        pixels.append(int(dados[i]))
        
    return largura, altura, valor_maximo, pixels


#histograma da imagem escala cinza
def gerar_histograma_cinza(nome_arquivo):
    
    resultado = ler_pgm(nome_arquivo)
    
    if resultado is None:
        return
    
    largura, altura, valor_maximo, pixels = resultado
    
    #criamos 256 posicoes, uma para cada intensidade
    histograma = []
    
    for i in range(256):
        histograma.append(0)
        
    #conta a quantidade de pixels e cada intensidade
    for pixel in pixels:
        histograma[pixel] += 1
        
    #gerar CSV
    arquivo_csv = open(
        "histograma_cinza.csv",
        "w",
        newline=""
    )

    escritor = csv.writer(arquivo_csv)

    escritor.writerow(["Intensidade", "Quantidade"])

    for intensidade in range(256):
        escritor.writerow([
            intensidade,
            histograma[intensidade]
        ])
    
    arquivo_csv.close()

    print("CSV da imagem Escala Cinza criado")


    #gerar grafico
    plt.figure()

    plt.bar(
        range(256),
        histograma
    )

    plt.title("Histograma-EscalaCinza")
    plt.xlabel("Intensidade")
    plt.ylabel("Quantidade de Pixels")

    plt.xlim(0,255)

    plt.show()


#funcao para ler imagem PPM P3
def ler_ppm(nome_arquivo):
    
    arquivo = open(nome_arquivo, "r")
    
    linhas = arquivo.readlines()
    
    arquivo.close()
    
    #remove comentarios e linhas vazias
    dados = []
    
    for linha in linhas:
        linha = linha.strip()
        
        if linha != "" and not linha.startswith("#"):
            dados.extend(linha.split())
            
    #primeiro valor deve ser P3
    formato = dados[0]
    
    if formato != "P3":
        print("Erro - o arquivo não é PPM P3")
        return None
    
    largura = int(dados[1])
    altura = int(dados[2])
    valor_maximo = int(dados[3])
    
    #separar canais RGB
    vermelho = []
    verde = []
    azul = []
    
    posicao = 4
    
    while posicao < len(dados):
        vermelho.append(int(dados[posicao]))
        verde.append(int(dados[posicao+1]))
        azul.append(int(dados[posicao+2]))
        
        posicao += 3
        
    return largura, altura, valor_maximo, vermelho, verde, azul

#histograma da imagem RGB
def gerar_histograma_rgb(nome_arquivo):

    resultado = ler_ppm(nome_arquivo)

    if resultado is None:
        return

    largura, altura, valor_maximo, vermelho, verde, azul = resultado

    #cria histograma
    histograma_r = []
    histograma_g = []
    histograma_b = []

    for i in range(256):
        histograma_r.append(0)
        histograma_g.append(0)
        histograma_b.append(0)

    #conta cada canal
    for pixel in vermelho:
        histograma_r[pixel] += 1

    for pixel in verde:
        histograma_g[pixel] += 1

    for pixel in azul:
        histograma_b[pixel] += 1

    #gera CSV
    arquivo_csv = open(
        "histograma_rgb.csv",
        "w",
        newline=""
    )

    escritor = csv.writer(arquivo_csv)

    escritor.writerow([
        "Intensidade",
        "Vermelho",
        "Verde",
        "Azul"
    ])

    for intensidade in range(256):
        escritor.writerow([
            intensidade,
            histograma_r[intensidade],
            histograma_g[intensidade],
            histograma_b[intensidade]
        ])

    arquivo_csv.close()

    print("CSV imagem RGB criado")

    #grafico canal vermelho
    plt.figure()

    plt.bar(
        range(256),
        histograma_r
    )

    plt.title("Histograma - Canal vermelho")
    plt.xlabel("Intensidade")
    plt.ylabel("Quantidade de Pixels")

    plt.xlim(0, 255)

    plt.show()

    #grafico canal verde
    plt.figure()

    plt.bar(
        range(256),
        histograma_g
    )

    plt.title("Histograma - Canal Verde")
    plt.xlabel("Intensidade")
    plt.ylabel("Quantidade de Pixels")

    plt.xlim(0, 255)

    plt.show()

    #grafico canal azul
    plt.figure()

    plt.bar(
        range(256),
        histograma_b
    )

    plt.title("Histograma - Canal Azul")
    plt.xlabel("Intensidade")
    plt.ylabel("Quantidade de Pixels")

    plt.xlim(0, 255)

    plt.show()
        
        
#Exec - Main

print("-----------Histograma de Imagens----------------")
print("------------------------------------------------")

print("\nImagem em escala de cinza:")

gerar_histograma_cinza(r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Exercicios_10092026\EntradaEscalaCinza.pgm")

print("Imagem RGB:")

gerar_histograma_rgb(r"C:\Users\Thinkpad\OneDrive\Documentos\IFC\ProcessamentoDigitalImagens\Atividade_Img_01\Exercicios_10092026\EntradaRGB.ppm")

print("Processo finalizado")