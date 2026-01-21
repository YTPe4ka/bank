#!/usr/bin/env python
"""Create proper .mo files from minimal data"""
import struct
import os

def create_mo_file(mo_path):
    """Create a minimal but valid .mo file"""
    
    # Create header with empty message catalog
    # Magic number (0xde120495)
    magic = 0xde120495
    # Version (0)
    version = 0
    # Number of strings (0 - empty catalog)
    num_strings = 0
    # Original string table offset (7*4 = 28)
    orig_table_offset = 28
    # Translation string table offset (28 + 0*8 = 28)
    trans_table_offset = 28
    # Hash table size (0)
    hash_size = 0
    # Hash table offset (0)
    hash_offset = 0
    
    # Write the .mo file
    with open(mo_path, 'wb') as f:
        # Write header
        f.write(struct.pack('<I', magic))
        f.write(struct.pack('<I', version))
        f.write(struct.pack('<I', num_strings))
        f.write(struct.pack('<I', orig_table_offset))
        f.write(struct.pack('<I', trans_table_offset))
        f.write(struct.pack('<I', hash_size))
        f.write(struct.pack('<I', hash_offset))

# Create minimal .mo files for all languages
os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
os.makedirs('locale/ru/LC_MESSAGES', exist_ok=True)
os.makedirs('locale/uz/LC_MESSAGES', exist_ok=True)

create_mo_file('locale/en/LC_MESSAGES/django.mo')
create_mo_file('locale/ru/LC_MESSAGES/django.mo')
create_mo_file('locale/uz/LC_MESSAGES/django.mo')

print('✓ Created minimal .mo files')
