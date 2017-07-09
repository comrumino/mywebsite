#!/usr/bin/env python2
''' module doc string'''
from __future__ import print_function
from os.path import dirname
import socket
import deveta

__all__ = ['DIR', 'INFO']


DIR = {}
DIR['assets'] = '/'.join([deveta.locate.parent_dir(), 'assets'])
DIR['template'] = '/'.join([DIR['assets'], 'template']) 
DIR['static'] = '/'.join([DIR['assets'], 'static'])
DIR['tmp'] = '/'.join([DIR['static'], 'tmp'])
DIR['partial'] = '/'.join([DIR['static'], 'partial'])
DIR['css'] = '/'.join([DIR['static'], 'css'])
DIR['js'] = '/'.join([DIR['static'], 'js'])
INFO = {}
INFO['host'] = 'stro.nz' if socket.gethostname() == 'zestronza' else '127.0.0.1'
