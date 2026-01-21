#!/usr/bin/env python
"""Generate .mo files from .po files"""
import struct
import os

def parse_po_file(po_file):
    """Parse a simple .po file"""
    messages = {'': ''}
    
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_msgid = None
    current_msgstr = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('msgid "'):
            if current_msgid and current_msgstr:
                messages[current_msgid] = current_msgstr
            current_msgid = line[7:-1]
            current_msgstr = None
        elif line.startswith('msgstr "'):
            current_msgstr = line[8:-1]
    
    if current_msgid and current_msgstr:
        messages[current_msgid] = current_msgstr
    
    return messages

def write_mo(mo_file, messages):
    """Write messages to .mo file in gettext format"""
    keys = sorted(messages.keys())
    offsets = []
    ids = b''
    strs = b''
    
    for key in keys:
        key_bytes = key.encode('utf-8')
        str_bytes = messages[key].encode('utf-8')
        offsets.append((len(ids), len(key_bytes), len(strs), len(str_bytes)))
        ids += key_bytes + b'\x00'
        strs += str_bytes + b'\x00'
    
    # Calculate header
    keyoffset = 7 * 4 + len(keys) * 8
    valueoffset = keyoffset + len(ids)
    koffsets = []
    voffsets = []
    
    for o_id, len_id, o_str, len_str in offsets:
        koffsets.append((len_id, keyoffset + o_id))
        voffsets.append((len_str, valueoffset + o_str))
    
    with open(mo_file, 'wb') as f:
        # Write header
        f.write(struct.pack('<I', 0xde120495))  # Magic number
        f.write(struct.pack('<I', 0))           # Version
        f.write(struct.pack('<I', len(keys)))   # Number of entries
        f.write(struct.pack('<I', 7*4))         # Offset of table with original strings
        f.write(struct.pack('<I', 7*4 + len(keys)*8))  # Offset of table with translated strings
        f.write(struct.pack('<I', 0))           # Size of hash table
        f.write(struct.pack('<I', 0))           # Offset of hash table
        
        # Write key table
        for length, offset in koffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write value table
        for length, offset in voffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write strings
        f.write(ids)
        f.write(strs)

# Convert .po files to .mo files
for lang in ['en', 'ru', 'uz']:
    po_file = f'locale/{lang}/LC_MESSAGES/django.po'
    mo_file = f'locale/{lang}/LC_MESSAGES/django.mo'
    
    if os.path.exists(po_file):
        messages = parse_po_file(po_file)
        write_mo(mo_file, messages)
        print(f'✓ Created {mo_file}')
    else:
        print(f'✗ File not found: {po_file}')
