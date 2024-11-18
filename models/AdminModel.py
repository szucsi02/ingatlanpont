from models.BejelentkezettFelhasznaloModel import BejelentkezettFelhasznaloModel


class AdminModel(BejelentkezettFelhasznaloModel):
    def __init__(self, id: int, email: str, jelszo: str, nev: str, telefonszam: str, kedvencek: list,
                 hirdetesek: list):
        super().__init__(id, email, True, jelszo, nev, telefonszam, kedvencek, hirdetesek)
