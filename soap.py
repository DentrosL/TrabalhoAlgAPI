import json
import re
import requests
import xml.etree.ElementTree as ET

URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

# Lista os códigos ISO e os nomes retornados pelo serviço em formato JSON
def listar():
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body>'
        '<ListOfCountryNamesByName xmlns="http://www.oorsprong.org/websamples.countryinfo" />'
        '</soap:Body>'
        '</soap:Envelope>'
    )

    try:
        resposta = requests.post(
            URL, data=xml, headers={"Content-Type": "text/xml"}, timeout=10
        )
        resposta.raise_for_status()
        raiz = ET.fromstring(resposta.text)

        # Cada registro precisa conter tanto o código ISO quanto o nome
        paises = []
        for registro in raiz.iter():
            codigo = nome = None
            for campo in registro:
                if campo.tag.endswith("sISOCode"):
                    codigo = (campo.text or "").strip()
                elif campo.tag.endswith("sName"):
                    nome = (campo.text or "").strip()
            if codigo and nome:
                paises.append(f"{codigo} - {nome}")

        if not paises:
            print("O serviço não retornou países em um formato reconhecido.")
            return None
        return json.dumps(paises, ensure_ascii=False, indent=2)
    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None
    except ET.ParseError:
        print("Erro ao processar a resposta XML.")
        return None


def validar_codigo_iso(codigo):
    # Normaliza e valida um código ISO antes de consultar o serviço
    codigo = codigo.strip().upper()
    if not re.fullmatch(r"[A-Z]{2}", codigo):
        raise ValueError("O código ISO deve conter exatamente duas letras.")
    return codigo

def capital(codigo):
    try:
        codigo = validar_codigo_iso(codigo)
    except (AttributeError, ValueError) as erro:
        print(f"Código ISO inválido: {erro}")
        return None
    # monta a mensagem SOAP com o código ISO informado
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body>'
        '<CapitalCity xmlns="http://www.oorsprong.org/websamples.countryinfo">'
        f'<sCountryISOCode>{codigo}</sCountryISOCode>'
        '</CapitalCity>'
        '</soap:Body>'
        '</soap:Envelope>'
    )

    try:
        # envia a requisição para o Web Service
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        # verifica se a requisição retornou algum erro HTTP
        resposta.raise_for_status()

        # converte a resposta XML para que possa ser analisada pelo Python
        raiz = ET.fromstring(resposta.text)

        # procura na resposta o elemento que contém o nome da capital
        for elemento in raiz.iter():
            if elemento.tag.endswith("CapitalCityResult"):
                return {
                    "codigo_iso": codigo,
                    "capital": elemento.text
                }

        # caso o país não seja encontrado na resposta
        print("País não encontrado.")
        return None

    # trata erros relacionados à conexão ou à requisição HTTP
    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    # trata erros caso a resposta não seja um XML válido
    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None

def moeda(codigo):
    try:
        codigo = validar_codigo_iso(codigo)
    except (AttributeError, ValueError) as erro:
        print(f"Código ISO inválido: {erro}")
        return None
    # monta a mensagem SOAP para consultar a moeda do país
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body>'
        '<CountryCurrency xmlns="http://www.oorsprong.org/websamples.countryinfo">'
        f'<sCountryISOCode>{codigo}</sCountryISOCode>'
        '</CountryCurrency>'
        '</soap:Body>'
        '</soap:Envelope>'
    )

    try:
        # envia a requisição para o Web Service
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        # verifica se a requisição retornou algum erro HTTP
        resposta.raise_for_status()

        # converte a resposta XML para ser analisada
        raiz = ET.fromstring(resposta.text)

        # dicionário que armazenará os dados retornados
        resultado = {}

        # procura na resposta o código da moeda
        for elemento in raiz.iter():
            if elemento.tag.endswith("sISOCode"):
                resultado["moeda"] = elemento.text

        resultado["codigo_iso"] = codigo

        return resultado

    # trata erros relacionados à conexão ou à requisição HTTP
    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    # trata erros caso a resposta não seja um XML válido
    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None


def codigo_telefone(codigo):
    try:
        codigo = validar_codigo_iso(codigo)
    except (AttributeError, ValueError) as erro:
        print(f"Código ISO inválido: {erro}")
        return None
    # monta a mensagem SOAP para consultar o código telefônico do país
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body>'
        '<CountryIntPhoneCode xmlns="http://www.oorsprong.org/websamples.countryinfo">'
        f'<sCountryISOCode>{codigo}</sCountryISOCode>'
        '</CountryIntPhoneCode>'
        '</soap:Body>'
        '</soap:Envelope>'
    )

    try:
        # envia a requisição para o Web Service.
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        # verifica se a requisição retornou algum erro HTTP e a linha 133 converte a resposta XML para ser analisada
        resposta.raise_for_status()
        raiz = ET.fromstring(resposta.text)

        # procura na resposta o elemento que contém o código telefônico
        for elemento in raiz.iter():
            if elemento.tag.endswith("CountryIntPhoneCodeResult"):
                return {
                    "codigo_iso": codigo,
                    "codigo_telefone": elemento.text
                }

    # trata erros relacionados à conexão ou à requisição HTTP
    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    # trata erros caso a resposta não seja um XML válido
    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None


def pais(codigo):
    try:
        codigo = validar_codigo_iso(codigo)
    except (AttributeError, ValueError) as erro:
        print(f"Código ISO inválido: {erro}")
        return None
    # cria um dicionário para reunir as informações do país
    resultado = {
        "codigo_iso": codigo
    }

    # realiza as consultas necessárias para obter os dados do país
    resultado_capital = capital(codigo)
    resultado_moeda = moeda(codigo)
    resultado_telefone = codigo_telefone(codigo)

    # adiciona a os dados ao dicionário caso a consulta tenha sido realizada
    if resultado_capital:
        resultado["capital"] = resultado_capital["capital"]
    if resultado_moeda:
        resultado["moeda"] = resultado_moeda["moeda"]
    if resultado_telefone:
        resultado["codigo_telefone"] = resultado_telefone["codigo_telefone"]

    return resultado


def main():
    print("INFO DO PAÍS")
    print("0 - Consultar lista de países")
    print("1 - Consultar país")
    print("2 - Consultar capital")
    print("3 - Consultar moeda")
    print("4 - Consultar código telefônico")
    print("5 - Sair")

    opcao = input("\nEscolha uma opção: ")
    if opcao in {"1", "2", "3", "4"}:
        codigo = input("Digite o código ISO do país: ").upper()

    # executa a função correspondente à opção escolhida
    if opcao == "0":
        resultado = listar()
    elif opcao == "1":
        resultado = pais(codigo)
    elif opcao == "2":
        resultado = capital(codigo)
    elif opcao == "3":
        resultado = moeda(codigo)
    elif opcao == "4":
        resultado = codigo_telefone(codigo)
    elif opcao == "5":
        print("Programa encerrado.")
        return
    else:
        print("Opção inválida.")
        return

    # exibe os dados retornados pelo Web Service
    if resultado:
        print("\nLISTA DE PAISES")

        # percorre o dicionário e exibe cada informação
        if opcao == "0":
            print(resultado)
        else:
            # percorre o dicionário e exibe cada informação
            for chave, valor in resultado.items():
                print(f"{chave}: {valor}")

main()