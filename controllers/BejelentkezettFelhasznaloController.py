from controllers.FelhasznaloController import FelhasznaloController


class BejelentkezettFelhasznaloController(FelhasznaloController):
    def profil_modosit(self, adat: str) -> None: pass
    def profil_torol(self, id: int) -> None: pass
    def sajat_hirdetes_hozzaad(self, hirdetes: 'HirdetesModel') -> None: pass
    def sajat_hirdetes_modosit(self, hirdetes_id: int) -> None: pass
    def sajat_hirdetes_torles(self, hirdetes_id: int) -> None: pass
    def sajat_hirdetes_listazas(self) -> None: pass