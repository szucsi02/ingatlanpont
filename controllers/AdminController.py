from controllers.BejelentkezettFelhasznaloController import BejelentkezettFelhasznaloController
from models import HirdetesModel


class AdminController(BejelentkezettFelhasznaloController):
    def hirdetes_listazas(self, hirdetes: HirdetesModel) -> None: pass
    def hirdetes_hozzaad(self, hirdetes: HirdetesModel) -> None: pass
    def hirdetes_modosit(self, hirdetes: HirdetesModel) -> None: pass
    def hirdetes_torles(self, hirdetes: HirdetesModel) -> None: pass