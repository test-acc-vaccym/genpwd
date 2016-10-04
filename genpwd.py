#!/usr/bin/env python3

import sys, shutil, os, os.path, hashlib, getpass

ALPHABET = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
BASE_COUNT = len(ALPHABET)
SECRET_FILE = os.path.expanduser("~/.genpwd")
INSTALL_PATH = "~/.local/bin/"
DEFAULT_PWD_LENGTH = 14 # Length of password

def get_random_base():
    return os.urandom(512)

# calculates SHA-512 as integer
def digest(msg):
    if type(msg) == str:
        msg = msg.encode('utf-8')
    elif type(msg) == int:
        msg = str(msg).encode('utf-8')
    return int(hashlib.sha512(msg).hexdigest(), 16)

# calculates digest of two messages by xor-ing them
def common_digest(msg1, msg2):
    msg1_d = digest(msg1)
    msg2_d = digest(msg2)
    return msg1_d ^ msg2_d

# base 58 encoding
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

# writes secret file to ~/.genpwd
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

# installs genpwd to ~/.local/bin/genpwd
def install():
    PATH = os.path.expanduser(INSTALL_PATH)
    FULL_PATH = "{}{}".format(PATH, "genpwd")
    # make sure ~/.local/bin exists
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    if os.path.exists(FULL_PATH):
        print("{}{} exists. Already installed?".format(INSTALL_PATH, "genpwd"))
    else:
        shutil.copy(sys.argv[0], FULL_PATH)
        print("Add this to your ~/.bashrc: 'export PATH=~/.local/bin/:$PATH'.")
        print("Then restart your terminal session or run the command from last line.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--install":
            install()
    else:
        run()
