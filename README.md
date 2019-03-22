# Festival de Curitiba

Scraper que baixa os eventos que acontecerão no [Festival de
Curitiba](http://festivaldecuritiba.com.br/) 2019.


## Licença

A licença do código é [LGPL3](). e dos dados [Creative Commons Attribution
ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/).
Caso utilize os dados, cite a fonte original e quem tratou os dados, como:
**Fonte: [site do Festival de Curitiba](http://festivaldecuritiba.com.br/),
dados tratados por Álvaro Justen/[Brasil.IO](https://brasil.io/)**.
Caso compartilhe os dados, utilize a mesma licença.


## Dados

Caso não queira rodar o script, [baixe os dados
diretamente](https://drive.google.com/open?id=1uPdutXB1uf_QVsmr2hfgT67uFR_5hYt6).


## Instalando

Para instalar as dependências você precisa de Python 3.7 em sua máquina.
Execute:

```bash
pip install -r requirements.txt
```


## Rodando

```bash
./run.sh
```

ou:

```bash
scrapy runspider --loglevel=INFO -o cwb.csv festival_csv.py
```
