#!/usr/bin/env python3

import os, os.path, hashlib, getpass

ALPHABET = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
BASE_COUNT = len(ALPHABET)
SECRET_FILE = ".genpwd"
DEFAULT_PWD_LENGTH = 14 # Length of password

def get_random_base():
    return os.urandom(512)

def digest(msg):
    if type(msg) == str:
        msg = msg.encode('utf-8')
    elif type(msg) == int:
        msg = str(msg).encode('utf-8')
    return int(hashlib.sha512(msg).hexdigest(), 16)

def common_digest(msg1, msg2):
    msg1_d = digest(msg1)
    msg2_d = digest(msg2)
    return msg1_d ^ msg2_d

def encode_digest(digest):
    encoded = ""
    if digest < 0:
        return ""
    while digest >= BASE_COUNT:
        encoded = "{}{}".format(ALPHABET[int(digest % BASE_COUNT)], encoded)
        digest = digest / BASE_COUNT
    if digest > 0:
        encoded = "{}{}".format(ALPHABET[int(digest)], encoded)
    return encoded

def setup():
    base_secret = get_random_base()
    with open(SECRET_FILE, 'wb') as f:
        f.write(base_secret)

# TODO: add special characters etc. so that most sites accept this password.
def normalize_password(pre_password):
    return pre_password

def run():
    if not os.path.exists(SECRET_FILE):
        setup()

    base_secret = None
    with open(SECRET_FILE, 'rb') as f:
        base_secret = f.read()

    brain_secret = getpass.getpass("Enter master password [will not echo]: ").strip()
    service_name = input("Enter service name [e.g. facebook.com]: ").strip()

    cmmn_digest = common_digest(common_digest(brain_secret, service_name), base_secret)

    # preliminary password
    pre_password = encode_digest(cmmn_digest)[:DEFAULT_PWD_LENGTH]
    password = normalize_password(pre_password)
    print(password)

if __name__ == "__main__":
    run()
