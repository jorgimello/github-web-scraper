# -*- coding: utf-8 -*-

from repositories_reader import read_repositories_file
from repositories_requester import request_repo

import requests
import re
from bs4 import BeautifulSoup

# 1. Carregar lista de repositórios
repos = read_repositories_file()

# Verifica se repositório está no formato <dono-do-projeto>/<nome-do-projeto>
# Evita requests em links existentes, mas que não são repositórios
def is_valid_repository(repository):
	words = repository.split('/')
	if len(words) == 2:
		return True
	return False

# Todo diretório contém apenas uma tabela, e nela pode ser encontrada os links para todos os outros diretórios e arquivos presentes no diretório
def extract_folder_content(url):
	response = request_url(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup.tbody


def extract_file_content(url):
	response = request_url(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	# TODO: finalizar web scraping de arquivo (linhas e bytes)
	pass

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