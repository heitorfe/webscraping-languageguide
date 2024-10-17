import requests
from bs4 import BeautifulSoup
import pandas as pd
import eng_to_ipa as ipa
import re
import os 

pd.set_option('display.max.rows', None)
pd.set_option('display.max.columns', None)
pd.set_option('display.max_colwidth', None)

def get_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    else:
        print(f"Erro ao acessar a página: {response.status_code}")
        return None

def get_vocabulary_urls():
    url = "https://www.languageguide.org/inglês/vocabulário/"
    
    soup = get_html(url)

    # Lista para armazenar os dados
    data = []
    
    # Itera sobre todas as divs com a classe 'section'
    for section in soup.find_all('div', class_='section'):
        # Pega o título da seção
        title_section = section.find('span', class_='title').get_text(strip=True)
        
        # Itera sobre os elementos com a classe 'category-link'
        category_links = section.find_all('div', class_='category-link')
        for link in category_links:
            # Pega o link e o texto dentro da categoria
            a_tag = link.find('a')
            if a_tag:
                href = f"https://www.languageguide.org{a_tag.get('href')}"
                text = a_tag.get_text(strip=True)
                data.append({
                    'type': 'category-link',
                    'section': title_section,
                    'subsection': text,
                    'url': href
                })
        
        # Verifica se existe algum link com a classe 'notepad2'
        notepad_links = section.find_all('a', class_='notepad2')
        if notepad_links:
            for notepad in notepad_links:
                notepad_href = f"https://www.languageguide.org{notepad.get('href')}"
                notepad_text = notepad.get_text(strip=True)
                data.append({
                    'type': 'notepad2',
                    'section': title_section,
                    'subsection': notepad_text,
                    'url': notepad_href
                })
        else:
            # Se não tiver 'notepad2', continue com os próximos 'category-link'
            for link in category_links:
                a_tag = link.find('a')
                if a_tag:
                    href = f"https://www.languageguide.org{a_tag.get('href')}"
                    text = a_tag.get_text(strip=True)
                    data.append({
                        'type': 'category-link',
                        'section': title_section,
                        'subsection': text,
                        'url': href
                    })
    
    # Cria um DataFrame
    df = pd.DataFrame(data, columns=['type', 'section', 'subsection', 'url'])
    return df.drop_duplicates()

def transform_urls(df):
    df.loc[13, 'subsection'] = 'The Skeleton(O esqueleto)'
    df.loc[138, 'subsection'] = 'Continents(Os continentes)'
    df.loc[139, 'subsection'] = 'Europe(Europa)'
    df.loc[:, 'subsection'] = df['subsection'].str.replace('(', ' (')
    df.loc[:, 'section'] = df['section'].str.replace('(', ' (')
    return df


def _split_concatenated_words(text):
    # Regex para separar entre minúsculas e maiúsculas
    split_text = re.findall(r'[A-Z][a-z]*', text)
    return split_text


def transform_words(df):
    # correção pontual
    df.loc[df['português'] == 'O olho <br> Os olhos', 'português'] = 'O olho'

    # count words
    df['count'] = df['inglês'].apply(lambda x: len(x.split(' ')))

    #separando palavras juntas
    condition = df['subseção']=='Europe (Europa)'
    df.loc[condition, 'inglês'] = df.loc[condition, 'inglês'].apply(_split_concatenated_words)
    df = df.explode('inglês').reset_index(drop=True)
    
    return df


def scrap_words(soup, subsection, section):
    data = []

    # Primeiro padrão: busca palavras e traduções dentro das tags <div>
    words = soup.find_all("div", class_="pop_up")
    translations = soup.find_all("div", class_="trans_popup")
    

    
    # Limpeza dos dados (remove espaços em branco e descarta valores vazios)
    words = [word.text.strip() for word in words if word.text.strip() != '']
    translations = [translation.text.strip() for translation in translations if translation.text.strip() != '']

    if not translations:
        translations = ['' for i in range(len(words))]
    
    # Adiciona os pares de palavra-tradução ao data (primeiro padrão)
    for word, translation in zip(words, translations):
        data.append({
            "seção": section,  
            "subseção": subsection,     
            "português": translation,
            "inglês": word,
            "ipa": ''  # Mantém o campo IPA vazio, se necessário preencher depois
        })
    
    # Segundo padrão: busca palavras e traduções dentro das tags <tr> e <td>
    rows = soup.find_all("tr", class_="audio")
    
    # Itera sobre cada linha (tr) para pegar os pares de palavra-tradução
    for row in rows:
        tds = row.find_all("td")

        # Verifica se há duas células (td), uma para a palavra e outra para a tradução
        if len(tds) >= 2:
            word = tds[0].find("span", class_="w").text.strip() if tds[0].find("span", class_="w") else None
            translation = tds[1].find("span", class_="translation").text.strip() if tds[1].find("span", class_="translation") else None
            
            # Se ambos forem encontrados, adiciona os dados à lista (segundo padrão)
            if word and translation:
                data.append({
                    "seção": section,  
                    "subseção": subsection,     
                    "português": translation,
                    "inglês": word,
                    "ipa": ''  # Deixe o campo IPA vazio
                })
    
    # Terceiro padrão: busca palavras e traduções dentro de tags <li> com classes específicas
    list_items = soup.find_all("tr", class_="audio")
    
    # Itera sobre os itens de lista (li) para pegar os pares de palavra-tradução
    for item in list_items:
        word = item.find("span", class_="word").text.strip() if item.find("span", class_="word") else None
        translation = item.find("span", class_="translation").text.strip() if item.find("span", class_="translation") else None
        
        # Se ambos forem encontrados, adiciona os dados à lista (terceiro padrão)
        if word and translation:
            data.append({
                "seção": section,
                "subseção": subsection,
                "português": translation,
                "inglês": word,
                "ipa": ''  # Deixe o campo IPA vazio
            })

    blockquotes = soup.find_all("blockquote")

    for blockquote in blockquotes:
        audio_divs = blockquote.find_all("div", class_="audio")
        
        for audio_div in audio_divs:
            word = audio_div.find("span", class_="w").text.strip() if audio_div.find("span", class_="w") else None
            translation = audio_div.find("span", class_="translation").text.strip() if audio_div.find("span", class_="translation") else None
            
            # Se ambos forem encontrados, adiciona os dados à lista (terceiro padrão)
            if word and translation:
                data.append({
                    "seção": section,  
                    "subseção": subsection,     
                    "português": translation,
                    "inglês": word,
                    "ipa": ''  # Deixe o campo IPA vazio
                })


    return data

def get_words(df):

    data = []
    for  _, row in df.iterrows():
        
        type = row['type']
        subsection = row['subsection']
        section = row['section']
        url = row['url']

        print(section, subsection)
    
        soup = get_html(url)
        register = scrap_words(soup, subsection, section)
        data = data + register
    return pd.DataFrame(data).drop_duplicates().reset_index(drop=True)


def transcribe_to_ipa(word):
    return ipa.convert(word)

def ipa_transform(df):
    
    condition = df['count'] <= 2  
    df.loc[condition, 'ipa']= df.loc[condition, 'inglês'].apply(transcribe_to_ipa)
    df['ipa_limpa'] = df['ipa'].str.replace(r"[ˈˈˌ*]", "", regex=True).replace(r'[^\w\s]', '', regex=True)
    
    df['ipa_limpa_reversa'] = df['ipa_limpa'].apply(lambda x: str(x)[::-1])
    df = df.sort_values(['count', 'ipa_limpa_reversa']).reset_index(drop=True)
    
    return df


data_files = os.listdir('data')

########################################## GET VOCABULARY URLS  ########################################## 
if 'urls.csv' in data_files:
    raw = pd.read_csv('data/urls.csv')

else:
    # get urls
    df_urls = get_vocabulary_urls()
    df_urls = transform_urls(df_urls)
    df_urls.to_csv('data/urls.csv', index=False)


########################################## GET WORDS  ########################################## 
# get words in each url
if 'raw.csv' in data_files:
    raw = pd.read_csv('data/raw.csv')

else:
    words_df = get_words(df_urls)
    df = transform_words(words_df)
    df.to_csv('data/raw.csv', index=False)

########################################## GET IPA   ########################################## 
if 'ipa.xlsx' in data_files:
    ipa_df = pd.read_excel('data/ipa.xlsx')
    
else:
    # getting IPA and save
    ipa_df = ipa_transform(df)
    ipa_df.to_excel('data/ipa.xlsx', index=False)