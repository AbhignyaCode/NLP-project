import re


class Stemmer:
    def __init__(self):
        self.b = bytearray()
        self.i = 0
        self.i_end = 0
        self.j = 0
        self.k = 0
        self.INC = 50
        self.vowel_pattern = re.compile(r"[aeiouy]")
        self.double_const_pattern = re.compile(r"[^aeiouy][aeiouy][^aeiouy]")
        self.end_patterns = {
            "sses": (-2, None),
            "ies": (-2, "i"),
            "eed": (-1, None),
            "ed": (None, None),
            "ing": (None, None),
            "ational": (7, "ate"),
            "tional": (6, "tion"),
            "enci": (4, "ence"),
            "anci": (4, "ance"),
            "izer": (4, "ize"),
            "bli": (3, "ble"),
            "alli": (4, "al"),
            "entli": (5, "ent"),
            "eli": (3, "e"),
            "ousli": (5, "ous"),
            "ization": (7, "ize"),
            "ation": (5, "ate"),
            "ator": (4, "ate"),
            "alism": (5, "al"),
            "iveness": (7, "ive"),
            "fulness": (7, "ful"),
            "ousness": (7, "ous"),
            "aliti": (5, "al"),
            "iviti": (5, "ive"),
            "biliti": (6, "ble"),
            "logi": (4, "log"),
            "icate": (5, "ic"),
            "ative": (5, ""),
            "alize": (5, "al"),
            "iciti": (5, "ic"),
            "ical": (4, "ic"),
            "ful": (3, ""),
            "ness": (4, ""),
        }

    def add(self, ch):
        self.b.extend(bytearray(ch, encoding="utf-8"))
        self.i += 1

    def add_word(self, w):
        self.b.extend(w.encode("utf-8"))
        self.i += len(w)

    def __str__(self):
        return self.b[: self.i_end].decode("utf-8")

    def get_result_length(self):
        return self.i_end

    def get_result_buffer(self):
        return self.b[: self.i_end]

    def cons(self, i):
        ch = self.b[i]
        return (
            ch != 97
            and ch != 101
            and ch != 105
            and ch != 111
            and ch != 117
            and (ch != 121 or (i == 0 or self.cons(i - 1)))
        )

    def m(self):
        n = 0
        i = 0
        while i <= self.j:
            if self.cons(i):
                i += 1
            else:
                break
        i += 1
        while True:
            while i <= self.j and not self.cons(i):
                i += 1
            if i > self.j:
                return n
            i += 1
            n += 1
            while i <= self.j and self.cons(i):
                i += 1
            if i > self.j:
                return n
            i += 1

    def vowel_in_stem(self):
        for i in range(self.j + 1):
            if not self.cons(i):
                return True
        return False

    def double_c(self, j):
        return j >= 1 and self.b[j] == self.b[j - 1] and self.cons(j)

    def cvc(self, i):
        return (
            i >= 2
            and self.cons(i)
            and not self.cons(i - 1)
            and self.cons(i - 2)
            and self.b[i] != 119
            and self.b[i] != 120
            and self.b[i] != 121
        )

    def ends(self, s):
        l = len(s)
        o = self.k - l + 1
        if o < 0:
            return False
        for i in range(l):
            if self.b[o + i] != ord(s[i]):
                return False
        self.j = self.k - l
        return True

    def set_to(self, s):
        l = len(s)
        o = self.j + 1
        for i in range(l):
            self.b[o + i] = ord(s[i])
        self.k = self.j + l

    def r(self, s):
        if self.m() > 0:
            self.set_to(s)

    def step1(self):
        if self.b[self.k] == 115:  # 's'
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.set_to("i")
            elif self.b[self.k - 1] != 115:
                self.k -= 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k -= 1
        elif self.ends("ed") or self.ends("ing"):
            if self.vowel_in_stem():
                self.k = self.j
                if self.ends("at"):
                    self.set_to("ate")
                elif self.ends("bl"):
                    self.set_to("ble")
                elif self.ends("iz"):
                    self.set_to("ize")
                elif self.double_c(self.k):
                    self.k -= 1
                    ch = self.b[self.k]
                    if ch == 108 or ch == 115 or ch == 122:
                        self.k += 1
                elif self.m() == 1 and self.cvc(self.k):
                    self.set_to("e")

    def step2(self):
        if self.ends("y") and self.vowel_in_stem():
            self.b[self.k] = 105  # 'i'

    def step3(self):
        if self.k == 0:
            return
        ch = self.b[self.k - 1]
        if ch == 97:  # 'a'
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif ch == 99:  # 'c'
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif ch == 101:  # 'e'
            if self.ends("izer"):
                self.r("ize")
        elif ch == 108:  # 'l'
            if self.ends("bli"):
                self.r("ble")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif ch == 111:  # 'o'
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif ch == 115:  # 's'
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif ch == 116:  # 't'
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif ch == 103:  # 'g'
            if self.ends("logi"):
                self.r("log")

    def step4(self):
        ch = self.b[self.k]
        if ch == 101:  # 'e'
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif ch == 105:  # 'i'
            if self.ends("iciti"):
                self.r("ic")
        elif ch == 108:  # 'l'
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif ch == 115:  # 's'
            if self.ends("ness"):
                self.r("")

    def step5(self):
        if self.k == 0:
            return
        ch = self.b[self.k - 1]
        if ch == 97:  # 'a'
            if not self.ends("al"):
                return
        elif ch == 99:  # 'c'
            if not self.ends("ance") and not self.ends("ence"):
                return
        elif ch == 101:  # 'e'
            if not self.ends("er"):
                return
        elif ch == 105:  # 'i'
            if not self.ends("ic"):
                return
        elif ch == 108:  # 'l'
            if not self.ends("able") and not self.ends("ible"):
                return
        elif ch == 110:  # 'n'
            if (
                not self.ends("ant")
                and not self.ends("ement")
                and not self.ends("ment")
                and not self.ends("ent")
            ):
                return
        elif ch == 111:  # 'o'
            if not (
                self.ends("ion")
                and (self.j >= 0)
                and (self.b[self.j] == 115 or self.b[self.j] == 116)
            ) and not self.ends("ou"):
                return
        elif ch == 115:  # 's'
            if not self.ends("ism"):
                return
        elif ch == 116:  # 't'
            if not self.ends("ate") and not self.ends("iti"):
                return
        elif ch == 117:  # 'u'
            if not self.ends("ous"):
                return
        elif ch == 118:  # 'v'
            if not self.ends("ive"):
                return
        elif ch == 122:  # 'z'
            if not self.ends("ize"):
                return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step6(self):
        self.j = self.k
        if self.b[self.k] == 101:  # 'e'
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k - 1)):
                self.k -= 1
        if self.b[self.k] == 108 and self.double_c(self.k) and self.m() > 1:
            self.k -= 1

    def stem(self):
        self.k = self.i - 1
        if self.k > 1:
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
        self.i_end = self.k + 1
        self.i = 0
