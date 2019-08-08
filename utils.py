# -*- coding: utf-8 -*-

def is_valid_repository(repository_string):
    # Verifica se repositório está no formato <dono-do-projeto>/<nome-do-projeto>
    # Evita requests em links existentes, mas que não estão no formato válido
    words = repository_string.split('/')
    if len(repository_string) >= 3 and len(words) == 2:
        return True
    return False

def calculate_bytes(size_unit_str):
    # Calcula bytes de um arquivo
    # Recebe uma string de tamanho 2 no formato 'size unit'
    try:
        size, unit = size_unit_str.split()
        print(size, unit)
        if unit == 'Bytes':
            return float(size)
        elif unit == 'KB':
            return float(size) * 1024.0
        elif unit == 'MB':
            return float(size) * 1024.0 * 1024.0
        else:
            return -1
    except ValueError:
        return -1