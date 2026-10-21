
import unittest

from phy import (
    hitung_jarak,
    hitung_waktu,
    hitung_ketinggian_maksimum,
)
from manuk import Manuk
from subproblem import subproblem_3, subproblem_4


class TestBoroSiManuk(unittest.TestCase):

    def test_jarak_contoh_buku(self):
        self.assertAlmostEqual(hitung_jarak(37, 10), 9.6, places=1)

    def test_waktu_contoh_buku(self):
        self.assertAlmostEqual(hitung_waktu(37, 100), 12.036, places=3)

    def test_ketinggian_contoh_buku(self):
        self.assertAlmostEqual(
            hitung_ketinggian_maksimum(37, 100),
            181.09,
            places=2,
        )

    def test_sudut_nol(self):
        self.assertAlmostEqual(hitung_jarak(0, 100), 0)
        self.assertAlmostEqual(hitung_waktu(0, 100), 0)
        self.assertAlmostEqual(hitung_ketinggian_maksimum(0, 100), 0)

    def test_kecepatan_nol(self):
        self.assertAlmostEqual(hitung_jarak(37, 0), 0)
        self.assertAlmostEqual(hitung_waktu(37, 0), 0)
        self.assertAlmostEqual(hitung_ketinggian_maksimum(37, 0), 0)

    def test_status_pohon(self):
        self.assertEqual(subproblem_3(37, 100, 100)[0], 1)
        self.assertEqual(subproblem_3(37, 100, 200)[0], 0)

    def test_banyak_burung(self):
        hasil = subproblem_4([
            (37, 100, 100),
            (37, 100, 200),
            (45, 50, 100),
            (30, 20, 10),
            (60, 40, 50),
        ])

        self.assertEqual(len(hasil), 5)
        self.assertEqual(
            [burung["status"] for burung in hasil],
            [1, 0, 0, 0, 1],
        )

    def test_batas_status(self):
        tinggi = hitung_ketinggian_maksimum(37, 100)
        burung = Manuk(37, 100, tinggi)
        self.assertEqual(burung.status_tabrakan(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
