# uncompyle6 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.9.16 (main, Mar  8 2023, 22:47:22) 
# [GCC 11.3.0]
# Embedded file name: parse_payload.py
import json, os, base64, hashlib, datetime, time, sys, argparse, struct

def u32(x):
    return struct.unpack('>I', x)[0]


def u64(x):
    return struct.unpack('>Q', x)[0]


def usage():
    print('Usage:******************* ')
    print('./parse_payload.py payload.bin')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='payload parse')
    parser.add_argument('payloadfile', type=(argparse.FileType('rb')), help='payload file name')
    args = parser.parse_args()
    filename = args.payloadfile.name
    magic = args.payloadfile.read(4)
    assert magic == b'CrAU'
    file_format_version = u64(args.payloadfile.read(8))
    assert file_format_version == 2
    manifest_size = u64(args.payloadfile.read(8))
    if file_format_version > 1:
        metadata_signature_size = u32(args.payloadfile.read(4))
    filename = args.payloadfile.name
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with open(filename, 'rb') as (f):
        while True:
            chunk = f.read(16384)
            if not chunk:
                break
            md5.update(chunk)
            sha256.update(chunk)

    payload_hash = base64.b64encode(sha256.digest()).decode()
    f.close()
    sha2 = hashlib.sha256()
    with open(filename, 'rb') as (w):
        chunk = w.read(manifest_size + 24)
        sha2.update(chunk)
    meta_hash = base64.b64encode(sha2.digest()).decode()
    w.close()
    param = {}
    other_param = {}
    param['link'] = ''
    param['hash'] = md5.hexdigest()
    other_param['FILE_HASH'] = payload_hash
    other_param['FILE_SIZE'] = str(os.path.getsize(filename))
    other_param['METADATA_HASH'] = meta_hash
    other_param['METADATA_SIZE'] = str(manifest_size + 24)
    print(other_param)
