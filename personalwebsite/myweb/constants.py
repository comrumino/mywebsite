#!/usr/bin/env python2
''' module doc string'''
from __future__ import print_function
import deveta

__all__ = ['DIR']

DIR = {}
DIR['assets'] = '/'.join([deveta.locate.parent_dir(), 'assets'])
DIR['template'] = '/'.join([DIR['assets'], 'template']) 
DIR['static'] = '/'.join([DIR['assets'], 'static'])
DIR['partial'] = '/'.join([DIR['static'], 'partial'])
DIR['css'] = '/'.join([DIR['static'], 'css'])
