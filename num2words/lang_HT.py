# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2024, William N. Havard.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA


from __future__ import print_function, unicode_literals
from .lang_EU import Num2Word_EU


class Num2Word_HT(Num2Word_EU):
    GIGA_SUFFIX = "ilya"
    MEGA_SUFFIX = "ilyon"

    def setup(self):
        Num2Word_EU.setup(self)

        self.negword = "mwens "
        self.pointword = "vigil"
        self.errmsg_nonnum = (
            u"Se nimewo sèlman ki ka konvèti an mo."
        )
        self.errmsg_toobig = (
            u"Nimewo twò gwo pou konvèti an mo (abs(%s) > %s)."
        )
        self.exclude_title = ["ey", "vigil", "mwens"]
        self.mid_numwords = [(1000, "mil"), (100, "san"),
                             (80, "katreven"), (60, "swasant"),
                             (50, "senkant"), (40, "karant"),
                             (30, "trant")]
        self.low_numwords = ["ven", "diznèf", "dizuit", "disèt",
                             "sèz", "kenz", "katòz", "trèz", "douz",
                             "onz", "dis", "nèf", "uit", "sèt", "sis",
                             "senk", "kat", "twa", "de", "en", "zewo"]


    def merge(self, curr, next):
        # Based on https://www.languagesandnumbers.com/comment-compter-en-creole-haitien/fr/hat/

        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum < 1000000:
                return next

        if nnum < cnum < 100:
            # Unit is one and ten number is different from 80
            if nnum % 10 == 1:
                # 20: add "t" before 1
                if cnum == 20:
                    ctext = ctext+'t'
                    return ("%sey%s" % (ctext, ntext), cnum + nnum)
                if cnum == 80:
                    return ("%sy%s" % (ctext, ntext), cnum + nnum)

            if cnum != 80:
                # 20: add "t" before 8 or 9
                if ctext.endswith('n') and nnum in [8, 9]:
                    ctext = ctext + "t"
                # 30,40,50,60: "nt" becomes "nn" except before 8 and 9
                if ctext.endswith(('nt', 'n')) and not nnum in [8, 9]:
                    ctext = ctext[:-1] if ctext.endswith('nt') else ctext
                    ctext = ctext + "n"
                return ("%s%s" % (ctext, ntext), cnum + nnum)
            return ("%s%s" % (ctext, ntext), cnum + nnum)
        # Nothing else above applies
        return ("%s %s" % (ctext, ntext), cnum + nnum)

    def to_ordinal(self, value):
        raise NotImplementedError

    def to_ordinal_num(self, value):
        raise NotImplementedError

    def to_currency(self, val, currency='EUR', cents=True, separator=' et',
                    adjective=False):
        raise NotImplementedError