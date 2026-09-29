import requests
import xml.etree.ElementTree as ET

URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

def capital(codigo):
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
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        resposta.raise_for_status()

        raiz = ET.fromstring(resposta.text)

        for elemento in raiz.iter():
            if elemento.tag.endswith("CapitalCityResult"):
                return {
                    "codigo_iso": codigo,
                    "capital": elemento.text
                }

    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None

def moeda(codigo):
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
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        resposta.raise_for_status()

        raiz = ET.fromstring(resposta.text)

        resultado = {}

        for elemento in raiz.iter():
            if elemento.tag.endswith("sISOCode"):
                resultado["moeda"] = elemento.text

        resultado["codigo_iso"] = codigo

        return resultado

    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None

def codigo_telefone(codigo):
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
        resposta = requests.post(
            URL,
            data=xml,
            headers={"Content-Type": "text/xml"},
            timeout=10
        )

        resposta.raise_for_status()

        raiz = ET.fromstring(resposta.text)

        for elemento in raiz.iter():
            if elemento.tag.endswith("CountryIntPhoneCodeResult"):
                return {
                    "codigo_iso": codigo,
                    "codigo_telefone": elemento.text
                }

    except requests.exceptions.RequestException:
        print("Erro ao conectar com o Web Service.")
        return None

    except ET.ParseError:
        print("Erro ao processar a resposta.")
        return None

def pais(codigo):
    resultado = {
        "codigo_iso": codigo
    }

    resultado_capital = capital(codigo)
    resultado_moeda = moeda(codigo)
    resultado_telefone = codigo_telefone(codigo)

    if resultado_capital:
        resultado["capital"] = resultado_capital["capital"]

    if resultado_moeda:
        resultado["moeda"] = resultado_moeda["moeda"]

    if resultado_telefone:
        resultado["codigo_telefone"] = resultado_telefone["codigo_telefone"]

    return resultado

def main():
    print("INFO DO PAÍS")
    print("1 - Consultar país")
    print("2 - Consultar capital")
    print("3 - Consultar moeda")
    print("4 - Consultar código telefônico")
    print("5 - Sair")

    opcao = input("\nEscolha uma opção: ")
    codigo = input("Digite o código ISO do país: ").upper()

    if opcao == "1":
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

    if resultado:
        print("\nINFORMAÇÕES DO PAÍS")

        for chave, valor in resultado.items():
            print(f"{chave}: {valor}")

main()