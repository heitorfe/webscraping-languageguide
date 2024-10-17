# Web Scraping para Agrupamento Fonético de Vocabulário em Inglês

Este projeto realiza a extração (web scraping) de vocabulário em inglês a partir do site [LanguageGuide.org](https://www.languageguide.org), transcreve as palavras para o Alfabeto Fonético Internacional (IPA), e agrupa as palavras de acordo com a fonética. O objetivo é facilitar a aprendizagem de vocabulário com uma abordagem que envolve a pronúncia correta.

## 📑 Funcionalidades
- **Extração de vocabulário**: Realiza scraping de palavras em inglês e suas respectivas traduções para português.
- **Agrupamento fonético**: Utiliza a biblioteca `eng_to_ipa` para transcrever palavras para o Alfabeto Fonético Internacional (IPA).
- **Organização por fonética**: Agrupa e ordena palavras com base na fonética, facilitando a navegação de vocabulário por sons similares.
- **Exportação de dados**: Salva o vocabulário extraído e transcrito para IPA em arquivos CSV e Excel.

## 🚀 Tecnologias Utilizadas
- **Python**: Linguagem de programação utilizada para todo o projeto.
- **Bibliotecas**:
  - `requests`: Para realizar requisições HTTP e obter o conteúdo HTML.
  - `BeautifulSoup` (via `bs4`): Para fazer parsing do HTML e extrair os dados desejados.
  - `Pandas`: Para manipulação e transformação de dados tabulares.
  - `eng_to_ipa`: Para converter palavras para a representação fonética (IPA).
  - `re`: Para manipulação de strings usando expressões regulares.
  
## 🔧 Configuração e Instalação

1. Clone este repositório para sua máquina local:
    ```bash
    git clone https://github.com/heitorfe/webscraping-languageguide.git
    ```

2. Instale as dependências necessárias:
    ```bash
    python -m venv venv
    venv/Scripts/activate.bat      #no Linux é venv/bin/activate
    pip install -r requirements.txt
    ```

Utilizei o Python 3.12.5 neste projeto

3. Execute o código:
    - O código coleta URLs de vocabulários, extrai palavras e transcreve-as para IPA.
    - Para rodar o projeto, execute o script `main.py`:
      ```bash
      python main.py
      ```

## 📂 Estrutura do Projeto
```
│
├── data/                     # Arquivos de dados gerados (urls.csv, raw.csv, ipa.xlsx)
├── main.py                   # Script principal para rodar o projeto
├── requirements.txt          # Lista de dependências do projeto
├── README.md                 # Documentação do projeto
```

### Principais Arquivos:
- **main.py**: O script principal que gerencia todo o fluxo do web scraping e transformação.
- **data/**: Diretório onde os arquivos de URLs, vocabulário cru, e dados finais transcritos são salvos.

## 📝 Como Funciona

1. **Coleta de URLs**: O script primeiro coleta todas as URLs de categorias de vocabulário no site [LanguageGuide.org](https://www.languageguide.org).
2. **Extração de Palavras**: Em cada URL, ele extrai as palavras em inglês e suas respectivas traduções para o português.
3. **Transcrição para IPA**: As palavras são transcritas para o IPA usando a biblioteca `eng_to_ipa`.
4. **Agrupamento por Fonética**: As palavras transcritas são organizadas por sons similares para ajudar no aprendizado focado em pronúncia.
5. **Exportação**: Todos os dados são exportados para arquivos CSV e Excel.

## 🛠️ Funções Principais

- `get_html(url)`: Faz a requisição HTTP e retorna o conteúdo HTML da página.
- `get_vocabulary_urls()`: Coleta URLs de diferentes categorias de vocabulário.
- `scrap_words(soup, subsection, section)`: Extrai palavras e suas traduções de uma página de vocabulário.
- `transcribe_to_ipa(word)`: Converte palavras em inglês para sua representação fonética no IPA.
- `ipa_transform(df)`: Agrupa as palavras por fonética e realiza a ordenação por som.

## 📊 Exemplos de Dados

- **URLs de vocabulário**: As URLs de cada categoria de vocabulário são coletadas e salvas em `data/urls.csv`.
- **Vocabulário extraído**: As palavras em inglês, suas traduções e a transcrição fonética são salvas em `data/raw.csv` e `data/ipa.xlsx`.

| Seção                        | Subseção                     | Português      | Inglês  | IPA   |
|------------------------------|------------------------------|----------------|---------|-------|
| The House (A casa)            | The House (A casa)           | o meio-fio     | curb    | kərb  |
| Miscellaneous (Assuntos diversos) | Shapes (As formas)      | o cubo         | cube    | kjub  |
| The House (A casa)            | The Bathroom 2 (O banheiro ii) | o tubo       | tube    | tub   |
| The Body (O corpo)            | Injuries (Os ferimentos)      | cicatriz, crosta | scab  | skæb  |


## 🧑‍💻 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões de melhorias ou encontrar algum bug, fique à vontade para abrir uma issue ou enviar um pull request.
