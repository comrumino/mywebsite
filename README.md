# A Python2 Library to Encapsulate a Personal Website

Personalwebsite is a pet project implemented in Python2 under GPL3.

![](misc/personalwebsite.gif?raw=true)

## Quick start

Personalwebsite is available as an Arch Linux pkgbuild and as a Python2 package. To make the package and install on Arch Linux ...
```
$ git clone "https://github.com/strayArch/personal-website.git"
$ cd personal-website/archlinux
$ makepkg
$ sudo pacman -U *pkg.tar.xz
$ sudo personalwebsite 
```
Then, to view the website visit it at [127.0.0.1](http://127.0.0.1/). For local development,
```
$ git clone "https://github.com/strayArch/personal-website.git"
$ printf "export PYTHONPATH=\'\${PYTHONPATH}:${PWD}/personal-website\'" >> ~/.bashrc && source ~/.bashrc
$ sudo ./personal-website/personalwebsite/server/server.py
```
