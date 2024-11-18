class BejelentkezettFelhasznaloModel:
    def __init__(self, id: int, email: str, admine: bool, jelszo: str, nev: str, telefonszam: str, kedvencek: list, hirdetesek: list):
        self._id = id
        self._email = email
        self._admine = admine
        self._jelszo = jelszo
        self._nev = nev
        self._telefonszam = telefonszam
        self._kedvencek = kedvencek
        self._hirdetesek = hirdetesek