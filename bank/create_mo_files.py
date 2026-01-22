#!/usr/bin/env python
"""
Скрипт для создания базовых .mo файлов для мультиязычной поддержки
"""
import os
import struct

def create_mo_file(path):
    """Создает базовый пустой .mo файл"""
    # Создаем пустой .mo файл с корректным заголовком
    # MO файл состоит из:
    # - Magic number (4 байта)
    # - Version (4 байта)
    # - Number of strings (4 байта)
    # - Offset of table with original strings (4 байта)
    # - Offset of table with translated strings (4 байта)
    # - Size of hash table (4 байта)
    # - Offset of hash table (4 байта)
    
    mo_content = struct.pack(
        'Iiiiiii',
        0xde120495,  # Magic number (little-endian)
        0,           # Version
        0,           # Number of strings
        28,          # Offset of table with original strings
        28,          # Offset of table with translated strings
        0,           # Size of hash table
        0            # Offset of hash table
    )
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(mo_content)
    print(f'✓ Created {path}')

# Создаем .mo файлы для всех языков
base_path = os.path.dirname(__file__)
languages = {
    'ru': 'Русский',
    'uz': 'Узбекский',
    'en': 'English'
}

for lang_code, lang_name in languages.items():
    mo_path = os.path.join(base_path, 'locale', lang_code, 'LC_MESSAGES', 'django.mo')
    create_mo_file(mo_path)

print('\n✓ All .mo files created successfully!')
