#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from glob import glob

import matplotlib.cm
import numpy as np

from ._version import __version__
from .cmapy import Cmapy

CMAPSFILE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'colormaps')
USER_CMAPFILE_DIR = os.environ.get('CMAP_DIR')


class Cmaps(object):
    """colormaps"""

    def __init__(self, ):
        self._cmap_d = dict()
        self._parse_cmaps()
        for cname in self._cmap_d.keys():
            setattr(self, cname, self._cmap_d[cname])
        self.__version__ = __version__

    def _listfname(self):
        cmapsflist = glob(os.path.join(CMAPSFILE_DIR, 'ncar_ncl/*.rgb')) + \
            glob(os.path.join(CMAPSFILE_DIR, 'self_defined/*.rgb'))
        if USER_CMAPFILE_DIR is not None:
            cmapsflist = cmapsflist + \
                glob(os.path.join(USER_CMAPFILE_DIR, '*.rgb'))
        return sorted(cmapsflist)

    def _coltbl(self, cmap_file):
        pattern = re.compile(r'(\d\.?\d*)\s+(\d\.?\d*)\s+(\d\.?\d*).*')
        with open(cmap_file) as cmap:
            cmap_buff = cmap.read()
        cmap_buff = re.compile('ncolors.*\n').sub('', cmap_buff)
        if re.search(r'\s*\d\.\d*', cmap_buff):
            return np.asarray(pattern.findall(cmap_buff), 'f4')
        else:
            return np.asarray(pattern.findall(cmap_buff), 'u1') / 255.

    def _parse_cmaps(self):
        for cmap_file in self._listfname():
            cname = os.path.basename(cmap_file).split('.rgb')[0]
            # start with the number will result illegal attribute
            if cname[0].isdigit():
                cname = 'N' + cname
            if '-' in cname:
                cname = cname.replace('-', '_')

            cmap = Cmapy(self._coltbl(cmap_file), name=cname)
            matplotlib.cm.register_cmap(name=cname, cmap=cmap)
            self._cmap_d[cname] = cmap

            cname = cname + '_r'
            cmap = Cmapy(self._coltbl(cmap_file)[::-1], name=cname)
            matplotlib.cm.register_cmap(name=cname, cmap=cmap)
            self._cmap_d[cname] = cmap

    def listcmname(self):
        for ii in (self._cmap_d.keys()):
            print(ii)

    def cmap_dict(self):
        return self._cmap_d
