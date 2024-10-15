import requests
from bs4 import BeautifulSoup
import pandas as pd
import eng_to_ipa as ipa

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

def transform(df):
    df.loc[13, 'subsection'] = 'The Skeleton(O esqueleto)'
    df.loc[138, 'subsection'] = 'Continents(Os continentes)'
    df.loc[139, 'subsection'] = 'Europe(Europa)'
    df.loc[:, 'subsection'] = df['subsection'].str.replace('(', ' (')
    df.loc[:, 'section'] = df['section'].str.replace('(', ' (')
    return df



def scrap_words(soup, subsection, section):
    data = []

    words = soup.find_all("div", class_="pop_up")
    translations = soup.find_all("div", class_="trans_popup")
    
    words = [word.text.strip() for word in words if word.text.strip() != '']
    translations = [translation.text.strip() for translation in translations if translation.text.strip() != '']
    
    for word, translation in zip(words, translations):
            # Adiciona os dados à lista
         data.append({
            "seção": section,  
            "subseção": subsection,     
            "português": translation,
            "inglês": word,
            "transcrição fonética": ''
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

df = get_vocabulary_urls()
df = transform(df)
words_df = get_words(df)

# get IPA
words_df['transcrição fonética']= words_df['inglês'].apply(transcribe_to_ipa)
words_df.to_excel('words.xlsx', index = False)