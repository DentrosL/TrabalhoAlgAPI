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

def main():
    print("INFO DO PAÍS")
    print("1 - Consultar país")
    print("2 - Consultar capital")
    print("3 - Consultar moeda")
    print("4 - Consultar código telefônico")
    print("5 - Sair")

    opcao = input("\nEscolha uma opção: ")
    codigo = input("Digite o código ISO do país: ").upper()

    if opcao == "2":
        resultado = capital(codigo)
    elif opcao == "5":
        print("Programa encerrado.")
        return
    else:
        print("Opção inválida.")
        return

    if resultado:

        for chave, valor in resultado.items():
            print(f"{chave}: {valor}")


main()