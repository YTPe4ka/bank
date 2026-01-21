import struct
import os

for lang in ['en', 'ru', 'uz']:
    mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
    
    # Create a minimal valid .mo file
    with open(mo_path, 'wb') as f:
        # MO file header (28 bytes)
        f.write(struct.pack('<I', 0xde120495))  # Magic number
        f.write(struct.pack('<I', 0))           # Version
        f.write(struct.pack('<I', 0))           # Number of entries
        f.write(struct.pack('<I', 28))          # Offset of table with original strings
        f.write(struct.pack('<I', 28))          # Offset of table with translated strings
        f.write(struct.pack('<I', 0))           # Size of hash table
        f.write(struct.pack('<I', 0))           # Offset of hash table
    
    print(f'Created {mo_path}')
