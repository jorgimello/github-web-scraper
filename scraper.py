# -*- coding: utf-8 -*-

from repositories_reader import read_repositories_file
from repositories_requester import request_url

import re
from bs4 import BeautifulSoup

# 1. Carregar lista de repositórios
repos = read_repositories_file()

def is_valid_repository(repository):
	# Verifica se repositório está no formato <dono-do-projeto>/<nome-do-projeto>
	# Evita requests em links existentes, mas que não estão no formato válido
	words = repository.split('/')
	if len(words) == 2:
		return True
	return False

def extract_folder_content(url):
	# Extrai conteúdo de um diretório
	# Retorna soup da tabela que contém os itens do diretório
	response = request_url(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup.tbody

FILE_CLASS_FINDER = 'text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0'
def extract_file_content(url):
	# Extrai conteúdo de um arquivo
	# TODO retornar apenas quantidade de linhas e tamanho do arquivo
	response = request_url(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup.find('div', class_=FILE_CLASS_FINDER).get_text().splitlines()

# extract_file_content('jorgimello/github-web-scraper/blob/master/repositories.txt')

PATH_TO_FOLDERS = '/tree/master'
PATH_TO_FILES = '/blob/master'
# 2. Realizar operações em cada repositório
# Operações: ler linhas, gerar árvore e salvar arquivo .txt
for r in repos:
	if not is_valid_repository(r):
		continue
	project_root_links = extract_folder_content(r)
	# Se lista não vazia, repositório existe
	if project_root_links:		
		folders = project_root_links.find_all(href=re.compile(r + PATH_TO_FOLDERS))
		files = project_root_links.find_all(href=re.compile(r + PATH_TO_FILES))
		for i in folders:
			print(i['href'])

		for j in files:
			print(j['href'])