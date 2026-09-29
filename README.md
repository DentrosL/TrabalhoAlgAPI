# Trabalho API
### Consulta de Informações de Países

> o usuário informa o código ISO do país, por exemplo `BR`, e o programa consulta o `Web Service` e monta um dicionário com as informações retornadas.

tipo:
```txt
CONSULTA DE PAÍSES

digite o código ISO do país: BR

informações do país
-------------------
país: Brasil
capital: Brasília
moeda: BRL
código telefônico: 55
continente: América do Sul
bandeira: http://...
````

cumprindo os quatro requisitos naturalmente:
```txt
Requisito --------------- Como cumprir
Web Service gratuito ---- CountryInfoService
Funções ----------------- capital(), moeda(), pais() etc.
Exceções ---------------- try/except para conexão, HTTP e XML
Dicionários ------------- Converter/organizar a resposta em dict
```

estrutura do dicionário:
```py
pais = {
    "codigo_iso": "",
    "nome": "",
    "capital": "",
    "codigo_telefone": "",
    "continente": "",
    "moeda": "",
    "bandeira": "",
    "idiomas": [
        {
            "codigo": "",
            "nome": ""
        }
    ]
}
```

2º menu exibido para o usuário:
```txt
INFO DO PAÍS

1 - Consultar país
2 - Consultar capital
3 - Consultar moeda
4 - Consultar código telefônico
5 - Sair

Escolha uma opção:
```