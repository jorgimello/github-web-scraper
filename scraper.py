# -*- coding: utf-8 -*-

from repositories_reader import read_repositories_file
from repositories_requester import request_url
from utils import is_valid_repository, calculate_bytes, get_folder_or_file_name, generate_str_with_spaces

import re
from bs4 import BeautifulSoup
from multiprocessing import Pool

def pull_folder_content(url):
    """Extrai conteúdo de um diretório
    Retorna soup.tbody da tabela que contém os itens do diretório
    """
    response = request_url(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.tbody

FILE_ELEMENT_FINDER = 'div'
FILE_CLASS_FINDER = 'text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0'
def pull_file_content(url):
    """Extrai conteúdo de um arquivo
    Retorna lista com informações do arquivo (linhas e bytes)
    """
    response = request_url(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find(FILE_ELEMENT_FINDER, class_=FILE_CLASS_FINDER)
    if div:
        return [t.strip() for t in div.get_text().splitlines() if t.strip() != '']
    else:
        return []

REGEX_TO_FOLDERS = '/tree/master'
REGEX_TO_FILES = '/blob/master'
def extract_hrefs(repository_content):
    """Extrai href de elementos que contenham links para diretórios e arquivos
    Retorna lista com os hrefs encontrados
    """
    folders_html = repository_content.find_all(href=re.compile(REGEX_TO_FOLDERS))
    files_html = repository_content.find_all(href=re.compile(REGEX_TO_FILES))
    hrefs_to_folders = [html['href'] for html in folders_html]
    hrefs_to_files = [html['href'] for html in files_html]
    return hrefs_to_folders, hrefs_to_files

def explore_repository(repo_name, depth=0):
    """Método principal da aplicação
    Percorre recursivamente o repositório
    TODO: armazenar tudo no .txt
    TODO: utilizar dict global para armazenar linhas e bytes dos arquivos
    """
    repository_content = pull_folder_content(repo_name)
    if (repository_content):
        folders, files = extract_hrefs(repository_content)
        for f in folders:
            print(generate_str_with_spaces(depth, get_folder_or_file_name(f), is_folder=True))            
            explore_repository(f, depth + 1)
        for f in files:
            print(generate_str_with_spaces(depth, get_folder_or_file_name(f), is_folder=False))
            pull_file_content(f)
        return
    else:
        return

if __name__ == '__main__':
    repo_names = read_repositories_file()
    valid_repos = [repo for repo in repo_names if is_valid_repository(repo)]
    if len(valid_repos) >= 2:
        with Pool(3) as p:
            # Explorar 3 repositórios paralelamente
            p.map(explore_repository, valid_repos)
    else:
        for valid_repo in valid_repos:
            explore_repository(valid_repo)

"""
Ideia de como armazenar extensões, linhas e bytes:
files = {'js': {'lines': 9, 'bytes': 15}, 'txt': {'lines': 10, 'bytes': 15}, 'yml': {'lines': 20, 'bytes': 30}}
files.keys() retorna extensões
usar <'extensao' in files> para verificar se extensão já existe. Ex: 'js' in files; 'py' in files
"""