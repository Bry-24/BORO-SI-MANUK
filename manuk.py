
"""
BORO SI MANUK
Module: manuk.py
Fungsi: Menyimpan data dan status simulasi burung.
"""

from dataclasses import dataclass
from phy import (
    hitung_jarak,
    hitung_waktu,
    hitung_ketinggian_maksimum,
)


@dataclass
class Manuk:
    sudut: float
    kecepatan_awal: float
    tinggi_pohon: float

    def jarak(self):
        return hitung_jarak(self.sudut, self.kecepatan_awal)

    def waktu_terbang(self):
        return hitung_waktu(self.sudut, self.kecepatan_awal)

    def ketinggian_maksimum(self):
        return hitung_ketinggian_maksimum(
            self.sudut, self.kecepatan_awal
        )

    def status_tabrakan(self):
        return int(
            self.ketinggian_maksimum() >= self.tinggi_pohon
        )
