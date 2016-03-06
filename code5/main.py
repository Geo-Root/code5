# -*- coding: utf-8 -*-
import sys
import os
import itertools
import json
import traceback
from code5.image.base import BaseImage

import six
from bisect import bisect_left

class Code5:

    def __init__(self, box_size=5, border=2,
                 image_factory=None):
        self.box_size = int(box_size)
        self.border = int(border)
        self.image_factory = image_factory
        if image_factory is not None:
            assert issubclass(image_factory, BaseImage)
        self.clear()

    def clear(self):
        """
        Reset the internal data.
        """
        self.data = []
        self.UL = "00000000"
        self.UR = "00000000"
        self.C = "00000000"
        self.DL = "00000000"
        self.DR = "00000000"

    def add_data(self, data):
        self.data = [int(d) for d in data.split('-')]
        pattern = Pattern()
        alphabet = pattern.patterns
        self.code = pattern.encode(self.data)
        self.blocks = []
        for d in self.data:
            for word in alphabet:
                if word['index'] == d:
                    self.blocks.append(word)
                    break


    def blocks2bin(self, blocks={}):
        binary = ['0','0','0','0','0','0','0','0']
        if '\\' in blocks['line1']:
            binary[0] = '1'
        if '|' in blocks['line1']:
            binary[1] = '1'
        if '/' in blocks['line1']:
            binary[2] = '1'
        if '—— +' in blocks['line2']:
            binary[7] = '1'
        if '+ ——' in blocks['line2']:
            binary[3] = '1'
        if '\\' in blocks['line3']:
            binary[4] = '1'
        if '|' in blocks['line3']:
            binary[5] = '1'
        if '/' in blocks['line3']:
            binary[6] = '1'
        return ''.join(binary)

    def revert(self, image_factory=None, image_path='', **kwargs):
        if image_factory is not None:
            assert issubclass(image_factory, BaseImage)
        else:
            image_factory = self.image_factory
            if image_factory is None:
                from code5.image.pil import PilImage
                image_factory = PilImage

        im = image_factory(
            self.border, 21, self.box_size, **kwargs)

        im.load(image_path)

        self.log = ""

        self.UL = ['0','0','0','0','0','0','0','0']
        self.UR = ['0','0','0','0','0','0','0','0']
        self.C = ['0','0','0','0','0','0','0','0']
        self.DL = ['0','0','0','0','0','0','0','0']
        self.DR = ['0','0','0','0','0','0','0','0']

        ULCenter = [3,3]
        URCenter = [3,18]
        CCenter = [11,11]
        DLCenter = [18,18]
        DRCenter = [18,3]

        if im.readrect(ULCenter[0]-1, ULCenter[1]-1) == 255 and im.readrect(ULCenter[0]-2, ULCenter[1]-2):
            self.UL[0] = '1'
        if im.readrect(ULCenter[0]-1, ULCenter[1]) == 255 and im.readrect(ULCenter[0]-2, ULCenter[1]):
            self.UL[1] = '1'
        if im.readrect(ULCenter[0]-1, ULCenter[1]+1) == 255 and im.readrect(ULCenter[0]-2, ULCenter[1]+2):
            self.UL[2] = '1'
        if im.readrect(ULCenter[0], ULCenter[1]+1) == 255 and im.readrect(ULCenter[0], ULCenter[1]+2):
            self.UL[3] = '1'
        if im.readrect(ULCenter[0]+1, ULCenter[1]+1) == 255 and im.readrect(ULCenter[0]+1, ULCenter[1]+2):
            self.UL[4] = '1'
        if im.readrect(ULCenter[0]+1, ULCenter[1]-1) == 255 and im.readrect(ULCenter[0]+2, ULCenter[1]-2):
            self.UL[5] = '1'
        if im.readrect(ULCenter[0]-1, ULCenter[1]) == 255 and im.readrect(ULCenter[0]-2, ULCenter[1]):
            self.UL[6] = '1'
        if im.readrect(ULCenter[0], ULCenter[1]-1) == 255 and im.readrect(ULCenter[0], ULCenter[1]-2):
            self.UL[7] = '1'
        
        if im.readrect(URCenter[0]-1, URCenter[1]-1) == 255 and im.readrect(URCenter[0]-2, URCenter[1]-2):
            self.UR[0] = '1'
        if im.readrect(URCenter[0]-1, URCenter[1]) == 255 and im.readrect(URCenter[0]-2, URCenter[1]):
            self.UR[1] = '1'
        if im.readrect(URCenter[0]-1, URCenter[1]+1) == 255 and im.readrect(URCenter[0]-2, URCenter[1]+2):
            self.UR[2] = '1'
        if im.readrect(URCenter[0], URCenter[1]+1) == 255 and im.readrect(URCenter[0], URCenter[1]+2):
            self.UR[3] = '1'
        if im.readrect(URCenter[0]+1, URCenter[1]+1) == 255 and im.readrect(URCenter[0]+1, URCenter[1]+2):
            self.UR[4] = '1'
        if im.readrect(URCenter[0]+1, URCenter[1]-1) == 255 and im.readrect(URCenter[0]+2, URCenter[1]-2):
            self.UR[5] = '1'
        if im.readrect(URCenter[0]-1, URCenter[1]) == 255 and im.readrect(URCenter[0]-2, URCenter[1]):
            self.UR[6] = '1'
        if im.readrect(URCenter[0], URCenter[1]-1) == 255 and im.readrect(URCenter[0], URCenter[1]-2):
            self.UR[7] = '1'

        if im.readrect(CCenter[0]-1, CCenter[1]-1) == 255 and im.readrect(CCenter[0]-2, CCenter[1]-2):
            self.C[0] = '1'
        if im.readrect(CCenter[0]-1, CCenter[1]) == 255 and im.readrect(CCenter[0]-2, CCenter[1]):
            self.C[1] = '1'
        if im.readrect(CCenter[0]-1, CCenter[1]+1) == 255 and im.readrect(CCenter[0]-2, CCenter[1]+2):
            self.C[2] = '1'
        if im.readrect(CCenter[0], CCenter[1]+1) == 255 and im.readrect(CCenter[0], CCenter[1]+2):
            self.C[3] = '1'
        if im.readrect(CCenter[0]+1, CCenter[1]+1) == 255 and im.readrect(CCenter[0]+1, CCenter[1]+2):
            self.C[4] = '1'
        if im.readrect(CCenter[0]+1, CCenter[1]-1) == 255 and im.readrect(CCenter[0]+2, CCenter[1]-2):
            self.C[5] = '1'
        if im.readrect(CCenter[0]-1, CCenter[1]) == 255 and im.readrect(CCenter[0]-2, CCenter[1]):
            self.C[6] = '1'
        if im.readrect(CCenter[0], CCenter[1]-1) == 255 and im.readrect(CCenter[0], CCenter[1]-2):
            self.C[7] = '1'

        if im.readrect(DLCenter[0]-1, DLCenter[1]-1) == 255 and im.readrect(DLCenter[0]-2, DLCenter[1]-2):
            self.DL[0] = '1'
        if im.readrect(DLCenter[0]-1, DLCenter[1]) == 255 and im.readrect(DLCenter[0]-2, DLCenter[1]):
            self.DL[1] = '1'
        if im.readrect(DLCenter[0]-1, DLCenter[1]+1) == 255 and im.readrect(DLCenter[0]-2, DLCenter[1]+2):
            self.DL[2] = '1'
        if im.readrect(DLCenter[0], DLCenter[1]+1) == 255 and im.readrect(DLCenter[0], DLCenter[1]+2):
            self.DL[3] = '1'
        if im.readrect(DLCenter[0]+1, DLCenter[1]+1) == 255 and im.readrect(DLCenter[0]+1, DLCenter[1]+2):
            self.DL[4] = '1'
        if im.readrect(DLCenter[0]+1, DLCenter[1]-1) == 255 and im.readrect(DLCenter[0]+2, DLCenter[1]-2):
            self.DL[5] = '1'
        if im.readrect(DLCenter[0]-1, DLCenter[1]) == 255 and im.readrect(DLCenter[0]-2, DLCenter[1]):
            self.DL[6] = '1'
        if im.readrect(DLCenter[0], DLCenter[1]-1) == 255 and im.readrect(DLCenter[0], DLCenter[1]-2):
            self.DL[7] = '1'

        if im.readrect(DRCenter[0]-1, DRCenter[1]-1) == 255 and im.readrect(DRCenter[0]-2, DRCenter[1]-2):
            self.DR[0] = '1'
        if im.readrect(DRCenter[0]-1, DRCenter[1]) == 255 and im.readrect(DRCenter[0]-2, DRCenter[1]):
            self.DR[1] = '1'
        if im.readrect(DRCenter[0]-1, DRCenter[1]+1) == 255 and im.readrect(DRCenter[0]-2, DRCenter[1]+2):
            self.DR[2] = '1'
        if im.readrect(DRCenter[0], DRCenter[1]+1) == 255 and im.readrect(DRCenter[0], DRCenter[1]+2):
            self.DR[3] = '1'
        if im.readrect(DRCenter[0]+1, DRCenter[1]+1) == 255 and im.readrect(DRCenter[0]+1, DRCenter[1]+2):
            self.DR[4] = '1'
        if im.readrect(DRCenter[0]+1, DRCenter[1]-1) == 255 and im.readrect(DRCenter[0]+2, DRCenter[1]-2):
            self.DR[5] = '1'
        if im.readrect(DRCenter[0]-1, DRCenter[1]) == 255 and im.readrect(DRCenter[0]-2, DRCenter[1]):
            self.DR[6] = '1'
        if im.readrect(DRCenter[0], DRCenter[1]-1) == 255 and im.readrect(DRCenter[0], DRCenter[1]-2):
            self.DR[7] = '1'

        self.log = self.log + str(self.UL)

        self.UL = ''.join(self.UL)
        self.UR = ''.join(self.UR)
        self.C = ''.join(self.C)
        self.DL = ''.join(self.DL)
        self.DR = ''.join(self.DR)

        data = [str(int(self.UL, 2)), str(int(self.UR, 2)), str(int(self.C, 2)), str(int(self.DL, 2)), str(int(self.DR, 2))]

        return '-'.join(data)

    def make(self):
        index = 0
        for d in self.blocks:
            if index == 0:
                self.UL = self.blocks2bin(d)
                self.ULd = d
            if index == 1:
                self.UR = self.blocks2bin(d)
                self.URd = d
            if index == 2:
                self.C = self.blocks2bin(d)
                self.Cd = d
            if index == 4:
                self.DL = self.blocks2bin(d)
                self.DLd = d
            if index == 3:
                self.DR = self.blocks2bin(d)
                self.DRd = d
            index = index + 1

    def dump_alphabet(self, image_factory=None, **kwargs):
        pattern = Pattern()
        for word in pattern.patterns:
            bin = self.blocks2bin(word)
            if image_factory is not None:
                assert issubclass(image_factory, BaseImage)
            else:
                image_factory = self.image_factory
                if image_factory is None:
                    from code5.image.pil import PilImage
                    image_factory = PilImage

            im = image_factory(
                self.border, 7, self.box_size, **kwargs)

            CCenter = [3,3]
            im.drawrect("#ff0000", CCenter[0], CCenter[1])
            for i in range(8):
                if bin[i] == '1':
                    if i == 1:
                        im.drawrect("black", CCenter[0]-1, CCenter[1])
                        im.drawrect("black", CCenter[0]-2, CCenter[1])
                        im.drawrect("black", CCenter[0]-3, CCenter[1])
                    if i == 2:
                        im.drawrect("black", CCenter[0]-1, CCenter[1]+1)
                        im.drawrect("black", CCenter[0]-2, CCenter[1]+2)
                        im.drawrect("black", CCenter[0]-3, CCenter[1]+3)
                    if i == 3:
                        im.drawrect("black", CCenter[0], CCenter[1]+1)
                        im.drawrect("black", CCenter[0], CCenter[1]+2)
                        im.drawrect("black", CCenter[0], CCenter[1]+3)
                    if i == 4:
                        im.drawrect("black", CCenter[0]+1, CCenter[1]+1)
                        im.drawrect("black", CCenter[0]+2, CCenter[1]+2)
                        im.drawrect("black", CCenter[0]+3, CCenter[1]+3)
                    if i == 5:
                        im.drawrect("black", CCenter[0]+1, CCenter[1])
                        im.drawrect("black", CCenter[0]+2, CCenter[1])
                        im.drawrect("black", CCenter[0]+3, CCenter[1])
                    if i == 6:
                        im.drawrect("black", CCenter[0]+1, CCenter[1]-1)
                        im.drawrect("black", CCenter[0]+2, CCenter[1]-2)
                        im.drawrect("black", CCenter[0]+3, CCenter[1]-3)
                    if i == 7:
                        im.drawrect("black", CCenter[0], CCenter[1]-1)
                        im.drawrect("black", CCenter[0], CCenter[1]-2)
                        im.drawrect("black", CCenter[0], CCenter[1]-3)
                    if i == 0:
                        im.drawrect("black", CCenter[0]-1, CCenter[1]-1)
                        im.drawrect("black", CCenter[0]-2, CCenter[1]-2)
                        im.drawrect("black", CCenter[0]-3, CCenter[1]-3)
            im.save("alphabet/%d.png"%word['index'])




    def make_image(self, image_factory=None, **kwargs):
        self.make()

        if image_factory is not None:
            assert issubclass(image_factory, BaseImage)
        else:
            image_factory = self.image_factory
            if image_factory is None:
                from code5.image.pil import PilImage
                image_factory = PilImage

        im = image_factory(
            self.border, 21, self.box_size, **kwargs)

        im.drawrect("#ff0000", 22, -1)
        im.drawrect("#ff0000", 22, -2)

        im.drawrect("#ff0000", -1, 22)
        im.drawrect("#ff0000", -2, 22)
        im.drawrect("#ff0000", 22, 22)
        im.drawrect("#ff0000", -1, -1)
        im.drawrect("#ff0000", -1, -2)
        im.drawrect("#ff0000", -2, -2)
        im.drawrect("#ff0000", -2, -1)

        for i in range(22):
            im.drawrect("black", i, -1)
            im.drawrect("black", i, -2)
            im.drawrect("black", i, 22)
            im.drawrect("black", -1, i)
            im.drawrect("black", -2, i)
            im.drawrect("black", 22, i)

        # UL
        ULCenter = [3,3]
        im.drawrect("#ff0000", ULCenter[0], ULCenter[1])
        for i in range(8):
            if self.UL[i] == '1':
                if i == 1:
                    im.drawrect("black", ULCenter[0]-1, ULCenter[1])
                    im.drawrect("black", ULCenter[0]-2, ULCenter[1])
                    # im.drawrect("black", ULCenter[0]-3, ULCenter[1])
                if i == 2:
                    im.drawrect("black", ULCenter[0]-1, ULCenter[1]+1)
                    im.drawrect("black", ULCenter[0]-2, ULCenter[1]+2)
                    # im.drawrect("black", ULCenter[0]-3, ULCenter[1]+3)
                if i == 3:
                    im.drawrect("black", ULCenter[0], ULCenter[1]+1)
                    im.drawrect("black", ULCenter[0], ULCenter[1]+2)
                    # im.drawrect("black", ULCenter[0], ULCenter[1]+3)
                if i == 4:
                    im.drawrect("black", ULCenter[0]+1, ULCenter[1]+1)
                    im.drawrect("black", ULCenter[0]+2, ULCenter[1]+2)
                    # im.drawrect("black", ULCenter[0]+1, ULCenter[1]+3)
                if i == 5:
                    im.drawrect("black", ULCenter[0]+1, ULCenter[1])
                    im.drawrect("black", ULCenter[0]+2, ULCenter[1])
                    # im.drawrect("black", ULCenter[0]+3, ULCenter[1])
                if i == 6:
                    im.drawrect("black", ULCenter[0]+1, ULCenter[1]-1)
                    im.drawrect("black", ULCenter[0]+2, ULCenter[1]-2)
                    # im.drawrect("black", ULCenter[0]+3, ULCenter[1]-3)
                if i == 7:
                    im.drawrect("black", ULCenter[0], ULCenter[1]-1)
                    im.drawrect("black", ULCenter[0], ULCenter[1]-2)
                    # im.drawrect("black", ULCenter[0], ULCenter[1]-3)
                if i == 0:
                    im.drawrect("black", ULCenter[0]-1, ULCenter[1]-1)
                    im.drawrect("black", ULCenter[0]-2, ULCenter[1]-2)
                    # im.drawrect("black", ULCenter[0]-3, ULCenter[1]-3)

        # UR
        URCenter = [3,18]
        im.drawrect("#ff0000", URCenter[0], URCenter[1])
        for i in range(8):
            if self.UR[i] == '1':
                if i == 1:
                    im.drawrect("black", URCenter[0]-1, URCenter[1])
                    im.drawrect("black", URCenter[0]-2, URCenter[1])
                    # im.drawrect("black", URCenter[0]-3, URCenter[1])
                if i == 2:
                    im.drawrect("black", URCenter[0]-1, URCenter[1]+1)
                    im.drawrect("black", URCenter[0]-2, URCenter[1]+2)
                    # im.drawrect("black", URCenter[0]-3, URCenter[1]+3)
                if i == 3:
                    im.drawrect("black", URCenter[0], URCenter[1]+1)
                    im.drawrect("black", URCenter[0], URCenter[1]+2)
                    # im.drawrect("black", URCenter[0], URCenter[1]+3)
                if i == 4:
                    im.drawrect("black", URCenter[0]+1, URCenter[1]+1)
                    im.drawrect("black", URCenter[0]+2, URCenter[1]+2)
                    # im.drawrect("black", URCenter[0]+3, URCenter[1]+3)
                if i == 5:
                    im.drawrect("black", URCenter[0]+1, URCenter[1])
                    im.drawrect("black", URCenter[0]+2, URCenter[1])
                    # im.drawrect("black", URCenter[0]+3, URCenter[1])
                if i == 6:
                    im.drawrect("black", URCenter[0]+1, URCenter[1]-1)
                    im.drawrect("black", URCenter[0]+2, URCenter[1]-2)
                    # im.drawrect("black", URCenter[0]+3, URCenter[1]-3)
                if i == 7:
                    im.drawrect("black", URCenter[0], URCenter[1]-1)
                    im.drawrect("black", URCenter[0], URCenter[1]-2)
                    # im.drawrect("black", URCenter[0], URCenter[1]-3)
                if i == 0:
                    im.drawrect("black", URCenter[0]-1, URCenter[1]-1)
                    im.drawrect("black", URCenter[0]-2, URCenter[1]-2)
                    # im.drawrect("black", URCenter[0]-3, URCenter[1]-3)
        
        # C
        CCenter = [11,11]
        im.drawrect("#ff0000", CCenter[0], CCenter[1])
        for i in range(8):
            if self.C[i] == '1':
                if i == 1:
                    im.drawrect("black", CCenter[0]-1, CCenter[1])
                    im.drawrect("black", CCenter[0]-2, CCenter[1])
                    # im.drawrect("black", CCenter[0]-3, CCenter[1])
                if i == 2:
                    im.drawrect("black", CCenter[0]-1, CCenter[1]+1)
                    im.drawrect("black", CCenter[0]-2, CCenter[1]+2)
                    # im.drawrect("black", CCenter[0]-3, CCenter[1]+3)
                if i == 3:
                    im.drawrect("black", CCenter[0], CCenter[1]+1)
                    im.drawrect("black", CCenter[0], CCenter[1]+2)
                    # im.drawrect("black", CCenter[0], CCenter[1]+3)
                if i == 4:
                    im.drawrect("black", CCenter[0]+1, CCenter[1]+1)
                    im.drawrect("black", CCenter[0]+2, CCenter[1]+2)
                    # im.drawrect("black", CCenter[0]+3, CCenter[1]+3)
                if i == 5:
                    im.drawrect("black", CCenter[0]+1, CCenter[1])
                    im.drawrect("black", CCenter[0]+2, CCenter[1])
                    # im.drawrect("black", CCenter[0]+3, CCenter[1])
                if i == 6:
                    im.drawrect("black", CCenter[0]+1, CCenter[1]-1)
                    im.drawrect("black", CCenter[0]+2, CCenter[1]-2)
                    # im.drawrect("black", CCenter[0]+3, CCenter[1]-3)
                if i == 7:
                    im.drawrect("black", CCenter[0], CCenter[1]-1)
                    im.drawrect("black", CCenter[0], CCenter[1]-2)
                    # im.drawrect("black", CCenter[0], CCenter[1]-3)
                if i == 0:
                    im.drawrect("black", CCenter[0]-1, CCenter[1]-1)
                    im.drawrect("black", CCenter[0]-2, CCenter[1]-2)
                    # im.drawrect("black", CCenter[0]-3, CCenter[1]-3)

        # DL
        DLCenter = [18,18]
        im.drawrect("#ff0000", DLCenter[0], DLCenter[1])
        for i in range(8):
            if self.DL[i] == '1':
                if i == 1:
                    im.drawrect("black", DLCenter[0]-1, DLCenter[1])
                    im.drawrect("black", DLCenter[0]-2, DLCenter[1])
                    # im.drawrect("black", DLCenter[0]-3, DLCenter[1])
                if i == 2:
                    im.drawrect("black", DLCenter[0]-1, DLCenter[1]+1)
                    im.drawrect("black", DLCenter[0]-2, DLCenter[1]+2)
                    # im.drawrect("black", DLCenter[0]-3, DLCenter[1]+3)
                if i == 3:
                    im.drawrect("black", DLCenter[0], DLCenter[1]+1)
                    im.drawrect("black", DLCenter[0], DLCenter[1]+2)
                    # im.drawrect("black", DLCenter[0], DLCenter[1]+3)
                if i == 4:
                    im.drawrect("black", DLCenter[0]+1, DLCenter[1]+1)
                    im.drawrect("black", DLCenter[0]+2, DLCenter[1]+2)
                    # im.drawrect("black", DLCenter[0]+3, DLCenter[1]+3)
                if i == 5:
                    im.drawrect("black", DLCenter[0]+1, DLCenter[1])
                    im.drawrect("black", DLCenter[0]+2, DLCenter[1])
                    # im.drawrect("black", DLCenter[0]+3, DLCenter[1])
                if i == 6:
                    im.drawrect("black", DLCenter[0]+1, DLCenter[1]-1)
                    im.drawrect("black", DLCenter[0]+2, DLCenter[1]-2)
                    # im.drawrect("black", DLCenter[0]+3, DLCenter[1]-3)
                if i == 7:
                    im.drawrect("black", DLCenter[0], DLCenter[1]-1)
                    im.drawrect("black", DLCenter[0], DLCenter[1]-2)
                    # im.drawrect("black", DLCenter[0], DLCenter[1]-3)
                if i == 0:
                    im.drawrect("black", DLCenter[0]-1, DLCenter[1]-1)
                    im.drawrect("black", DLCenter[0]-2, DLCenter[1]-2)
                    # im.drawrect("black", DLCenter[0]-3, DLCenter[1]-3)

        # DR
        DRCenter = [18,3]
        im.drawrect("#ff0000", DRCenter[0], DRCenter[1])
        for i in range(8):
            if self.DR[i] == '1':
                if i == 1:
                    im.drawrect("black", DRCenter[0]-1, DRCenter[1])
                    im.drawrect("black", DRCenter[0]-2, DRCenter[1])
                    # im.drawrect("black", DRCenter[0]-3, DRCenter[1])
                if i == 2:
                    im.drawrect("black", DRCenter[0]-1, DRCenter[1]+1)
                    im.drawrect("black", DRCenter[0]-2, DRCenter[1]+2)
                    # im.drawrect("black", DRCenter[0]-3, DRCenter[1]+3)
                if i == 3:
                    im.drawrect("black", DRCenter[0], DRCenter[1]+1)
                    im.drawrect("black", DRCenter[0], DRCenter[1]+2)
                    # im.drawrect("black", DRCenter[0], DRCenter[1]+3)
                if i == 4:
                    im.drawrect("black", DRCenter[0]+1, DRCenter[1]+1)
                    im.drawrect("black", DRCenter[0]+2, DRCenter[1]+2)
                    # im.drawrect("black", DRCenter[0]+3, DRCenter[1]+3)
                if i == 5:
                    im.drawrect("black", DRCenter[0]+1, DRCenter[1])
                    im.drawrect("black", DRCenter[0]+2, DRCenter[1])
                    # im.drawrect("black", DRCenter[0]+3, DRCenter[1])
                if i == 6:
                    im.drawrect("black", DRCenter[0]+1, DRCenter[1]-1)
                    im.drawrect("black", DRCenter[0]+2, DRCenter[1]-2)
                    # im.drawrect("black", DRCenter[0]+3, DRCenter[1]-3)
                if i == 7:
                    im.drawrect("black", DRCenter[0], DRCenter[1]-1)
                    im.drawrect("black", DRCenter[0], DRCenter[1]-2)
                    # im.drawrect("black", DRCenter[0], DRCenter[1]-3)
                if i == 0:
                    im.drawrect("black", DRCenter[0]-1, DRCenter[1]-1)
                    im.drawrect("black", DRCenter[0]-2, DRCenter[1]-2)
                    # im.drawrect("black", DRCenter[0]-3, DRCenter[1]-3)
        
        return im

class Pattern:
    def __init__(self):
        self.number = 0
        self.possibilities()

    def partitions(self, items, n):
        if n == 1:
            return [set([e]) for e in items]
        results = self.partitions(items, n - 1)
        for i, j in itertools.combinations(range(len(results)), 2):
            newresult = results[i] | results[j]
            if newresult not in results:
                results.append(newresult)
        return results

    def print_center(self, blocks=[0,0,0,0,0,0,0,0]):
        line1 = ""
        line2 = ""
        line3 = ""

         # line1
        if blocks[0] == 0:
            line1 += "  "
        else:
            line1 += " \\"
            # line1 += " *"
        if blocks[1] == 0:
            line1 += "   "
        else:
            line1 += " | " 
        if blocks[2] == 0:
            line1 += "  "
        else:
            line1 += "/ " 

        # line2
        if blocks[3] == 0:
            line2 += "   +"
        else:
            line2 += "—— +"
        if blocks[4] == 0:
            line2 += "   "
        else:
            line2 += " ——"

        # line3
        if blocks[5] == 0:
            line3 += "  "
        else:
            line3 += " /"
        if blocks[6] == 0:
            line3 += "   "
        else:
            line3 += " | " 
        if blocks[7] == 0:
            line3 += "  "
        else:
            line3 += "\\ "
            # line1 += " *"

        return [line1, line2, line3]


    def encode(self, blocks=[0,0,0,0,0]):
        el1 = {}
        el2 = {}
        el3 = {}
        el4 = {}
        el5 = {}
        for el in self.patterns:
            if el['index'] == blocks[0]:
                el1 = el
            if el['index'] == blocks[1]:
                el2 = el
            if el['index'] == blocks[2]:
                el3 = el
            if el['index'] == blocks[3]:
                el4 = el
            if el['index'] == blocks[4]:
                el5 = el
        line1 = el1['line1']+"       "+el2['line1']
        line2 = el1['line2']+"       "+el2['line2']
        line3 = el1['line3']+"       "+el2['line3']
        line5 = "       "+el3['line1']
        line6 = "       "+el3['line2']
        line7 = "       "+el3['line3']
        line9 = el4['line1']+"       "+el5['line1']
        line10 = el4['line2']+"       "+el5['line2']
        line11 = el4['line3']+"       "+el5['line3']

        return [line1, line2, line3, line5, line6, line7, line9, line10, line11]

    def encode_single(self, block=0):
        element = {}
        for el in self.patterns:
            if el['index'] == block:
                element = el

        line1 = element['line1']
        line2 = element['line2']
        line3 = element['line3']

        return [line1, line2, line3]

    def possibilities(self, printed=False):

        items = [0,1,2,3,4,5,6,7]

        # for size in range(8):
        # print "Size: %d"%size
        gen = {}
        gen['1']=[]
        gen['2']=[]
        gen['3']=[]
        gen['3']=[]
        gen['4']=[]
        gen['5']=[]
        gen['6']=[]
        gen['7']=[]
        gen['8']=[]

        self.patterns = []

        results = self.partitions(items, 7)
        for result in results:
            if len(result) == 1:
                gen['1'].append(result)
            if len(result) == 2:
                gen['2'].append(result)
            if len(result) == 3:
                gen['3'].append(result)
            if len(result) == 4:
                gen['4'].append(result)
            if len(result) == 5:
                gen['5'].append(result)
            if len(result) == 6:
                gen['6'].append(result)
            if len(result) == 7:
                gen['7'].append(result)
            if len(result) == 8:
                gen['8'].append(result)

        lines = self.print_center([0,0,0,0,0,0,0,0])

        self.patterns.append({'index':0, 'line1':lines[0], 'line2':lines[1], 'line3':lines[2]})
        possible = 1
        for count, generated in gen.iteritems():
            # print "Size: %s"%count
            for state in generated:
                blocks = [0,0,0,0,0,0,0,0]
                for index in state:
                    blocks[index] = 1
                lines = self.print_center(blocks)
                if printed:
                    print "---%d---"%(possible)
                    for line in lines:
                        print line
                    print "\n"
                self.patterns.append({'index':possible, 'line1':lines[0], 'line2':lines[1], 'line3':lines[2]})
                possible += 1

    def decode_single(self, lines=[]):
        try:
            possibles = self.patterns
            for possible in possibles:
                if possible['line1'] == lines[0].encode('utf-8'):
                    if possible['line2'] == lines[1].encode('utf-8'):
                        if possible['line3'] == lines[2].encode('utf-8'):
                            return possible['index']
            return -1
        except:
            traceback.print_exc()
            return -1

    def decode(self, lines=[]):
        raws = []

        el1 = [lines[0][0:7],lines[1][0:7],lines[2][0:7]]
        el2 = [lines[0][14:21],lines[1][14:21],lines[2][14:21]]

        el3 = [lines[3][7:14],lines[4][7:14],lines[5][7:14]]

        el4 = [lines[6][0:7],lines[7][0:7],lines[8][0:7]]
        el5 = [lines[6][14:21],lines[7][14:21],lines[8][14:21]]

        print el1
        print el2
        print el3
        print el4
        print el5
        
        result = []

        result.append(self.decode_single(el1))
        result.append(self.decode_single(el2))
        result.append(self.decode_single(el3))
        result.append(self.decode_single(el4))
        result.append(self.decode_single(el5))

        return "%d-%d-%d-%d-%d"%(result[0],result[1],result[2],result[3],result[4])

    def decode_2(self, lines=[]):
        
        result = []

        result.append(self.decode_single(lines[0]))
        result.append(self.decode_single(lines[1]))
        result.append(self.decode_single(lines[2]))
        result.append(self.decode_single(lines[3]))
        result.append(self.decode_single(lines[4]))

        return "%d-%d-%d-%d-%d"%(result[0],result[1],result[2],result[3],result[4])