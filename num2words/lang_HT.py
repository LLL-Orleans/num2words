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
    CURRENCY_FORMS = {
        'EUR': (('euro', 'euro'), ('sant', 'santim')),
        'USD': (('dola', 'dola'), ('sant', 'santim')),
        'FRF': (('fran', 'frans'), ('sant', 'santim')),
        'GBP': (('liv', 'liv'), ('penny', 'pence')),
        'CNY': (('yuan', 'yuans'), ('fen', 'jiaos')),
        'HTG': (('goud', 'goud'), ('santim', 'santim')),
    }

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

        self.ords = {
            "de": "dezyem",
            "twa": "twazyem",
            "kat": "katriyem",
            "sis": "sizyem",
            "nèf": "nèvyem",
            "dis": "dizyem",
            "san": "santyem"
        }

    def merge(self, curr, next):
        # Based on https://www.languagesandnumbers.com/comment-compter-en-creole-haitien/fr/hat/
        # Example 1:
        # curr = ("trant", 30), next = ("senk", 5)
        # Output: ("trannsenk", 35) -> trantsenk would also be acceptable

        # Example 2:
        # curr = ("swasant", 60), next = ("uit", 8)
        # Output: ("swasantuit", 68)

        # Example 3:
        # curr = ("ven", 20), next = ("en", 1)
        # Output: ("venteyen", 21)

        # Example 4:
        # curr = ("mil", 1000), next = ("san", 100)
        # Output: ("mil san", 1100)

        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum < 1000000:
                return next

        if nnum < cnum < 100:
            # Unit is one and ten number is different from 80
            if nnum % 10 == 1:
                # "20" becomes "20t" before 1
                if cnum == 20:
                    ctext = ctext+'t' # 21=venteyen and not venten
                return ("%sey%s" % (ctext, ntext), cnum + nnum)

            if cnum != 80:
                # 20: add "t" before 8 or 9
                if ctext.endswith('n') and nnum in [8, 9]:
                    ctext = ctext + "t"
                # 30,40,50,60: "nt" becomes "nn" except before 8 and 9
                if ctext.endswith(('nt', 'n')) and not nnum in [8, 9]:
                    ctext = ctext[:-1] if ctext.endswith('nt') else ctext
                    ctext = ctext + "n"
            return ("%s%s" % (ctext, ntext), cnum + nnum)

        # If the next number is larger and is a multiple of 100
        if nnum > cnum and nnum % 100 == 0:
            # One becomes yon (instead of en) if billion or million
            if (nnum % 1_000_000 == 0 or nnum % 1_000_000_000 == 0) and cnum == 1:
                ctext = "yon"
            # if multiple of a 100 and unit number is 6 or 8, remove the last letter
            if cnum in [6,8]:
                # sis san / uit san -> si san / ui san
                ctext = ctext[:-1]

        return ("%s %s" % (ctext, ntext), cnum + nnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)  # Ensure value is valid for ordinal conversion

        # Special case for 1 (premier becomes "premye" in Creole)
        if value == 1:
            return "premye"

        # Convert cardinal to word (e.g., 2 -> "de", 3 -> "twa")
        word = self.to_cardinal(value)

        # Haitian Creole ordinals (irregular suffix replacements)
        for src, repl in self.ords.items():
            if word.endswith(src):
                word = word[:-len(src)] + repl
                break
        else:
            # General case: Add "yèm" to form the ordinal
            if word[-1] == "e":
                word = word[:-1]  # Remove final "e" before adding "yèm"
            word = word + "yèm"

        return word

    def to_ordinal_num(self, value):
        """
        Converts a number to its ordinal numerical representation in Haitian Creole.

        Arguments:
        value -- the integer to convert.

        Returns:
        The ordinal number as a string.

        Example:
        - 1 becomes "1er"
        - 2 becomes "2yèm"
        - 10 becomes "10yèm"
        """

        self.verify_ordinal(value)  # Ensure value is valid for ordinal conversion

        # Start with the cardinal number as a string
        out = str(value)

        # Special case: "1" becomes "1er" (premier)
        if value == 1:
            out += "er"
        else:
            # For all other numbers, append "yèm" (e.g., 2 -> "2yèm")
            out += "yèm"

        return out

    def to_currency(self, val, currency='EUR', cents=True, separator=' ey',
                    adjective=False):
        result = super(Num2Word_HT, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)
        return result