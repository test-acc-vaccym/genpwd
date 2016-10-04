# genpwd
A password manager (?) which does not store your passwords on disk and provides plausible deniability.

## Dependencies
* Python 3.x

## Usage
```
git clone https://github.com/oompf/genpwd.git
cd genpwd
./genpwd
```

## How it works
On first usage of this software a .genpwd file is created in your home directory which contains only some 512-byte randomness and **not** your passwords.
To generate a password you must enter your **master password** and the service name, e.g. google.com, github.com, facebook.com etc.

With a bit of mathematics, the algorithm always produces the same passwords without storing them on your disk.

Keep this things in mind:
  * Use a free and open-source operating system (e.g. Arch Linux[https://wwww.archlinux.org/]).
  * **Backup your .genpwd and remember your master password** as they are needed for password generation.
  * This software may change at any time without staying backward compatible.
  * This software **has not been audited** yet and **may not satisfy current cryptographic standards**.
  * **Change the access rights** for .genpwd and genpwd.py so that only you have access.
