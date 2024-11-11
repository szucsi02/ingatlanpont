

class Hirdetes():
    def __init__(self, telekmeret: int, cim: str, id: int, ar: int, leiras: str, kepek: list, nev: str, szobak_szama: int, alapterulet: int, hirdeto: 'BejelentkezettFelhasznaloModel'):
        self._telekmeret = telekmeret
        self._cim = cim
        self._id = id
        self._ar = ar
        self._leiras = leiras
        self._kepek = kepek
        self._nev = nev
        self._szobak_szama = szobak_szama
        self._alapterulet = alapterulet
        self._hirdeto = hirdeto