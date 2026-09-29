# Trabalho API
### Consulta de Informações de Países

> o usuário informa o código ISO do país, por exemplo `BR`, e o programa consulta o `Web Service` e monta um dicionário com as informações retornadas.

cumprindo os quatro requisitos naturalmente:
```txt
Requisito --------------- Como cumprir
Web Service gratuito ---- CountryInfoService
Funções ----------------- capital(), moeda(), codigo_telefone() e pais()
Exceções ---------------- try/except para conexão, HTTP e XML
Dicionários ------------- Converter/organizar a resposta em dict
```

estrutura do dicionário:
```py
pais = {
    "codigo_iso": "",
    "capital": "",
    "codigo_telefone": "",
    "moeda": ""
}
```

menu exibido para o usuário:
```txt
INFO DO PAÍS

1 - Consultar país
2 - Consultar capital
3 - Consultar moeda
4 - Consultar código telefônico
5 - Sair

Escolha uma opção:
```

resultado final esperado:
```txt
INFO DO PAÍS
1 - Consultar país
2 - Consultar capital
3 - Consultar moeda
4 - Consultar código telefônico
5 - Sair

Escolha uma opção: 1
Digite o código ISO do país: br

INFORMAÇÕES DO PAÍS
codigo_iso: BR
capital: Brasilia
moeda: BRL
codigo_telefone: 55
```

> **Para mais conteúdo do trabalho**:
[Docs da pesquisa](https://docs.google.com/document/d/1i_4jy7rltkIc6atRYiH27vp9qzsAapGPHLJ1sz7XYgI/edit?usp=sharing)