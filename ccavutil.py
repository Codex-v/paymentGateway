#!/usr/bin/env python

from Crypto.Cipher import AES
import hashlib

def pad(data):
    length = 16 - (len(data) % 16)
    padding = bytes([length] * length)
    return data + padding

def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText.encode('utf-8'))  # Convert string to bytes and pad
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode('utf-8'))
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText).hex()
    return encryptedText

def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode('utf-8'))
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
    decryptedText = dec_cipher.decrypt(bytes.fromhex(cipherText)).decode('utf-8')

    # Remove PKCS#7 padding
    pad_length = ord(decryptedText[-1])
    decryptedText = decryptedText[:-pad_length]

    return decryptedText