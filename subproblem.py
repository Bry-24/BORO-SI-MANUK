
"""
BORO SI MANUK
Module: subproblem.py
Fungsi: Menangani penyelesaian subsoal 1 sampai 4.
"""

from manuk import Manuk


def subproblem_1(sudut, kecepatan_awal):
    burung = Manuk(sudut, kecepatan_awal, 0)
    return burung.jarak()


def subproblem_2(sudut, kecepatan_awal):
    burung = Manuk(sudut, kecepatan_awal, 0)
    return burung.waktu_terbang()


def subproblem_3(sudut, kecepatan_awal, tinggi_pohon):
    burung = Manuk(sudut, kecepatan_awal, tinggi_pohon)
    return burung.status_tabrakan(), burung.ketinggian_maksimum()


def subproblem_4(data_burung):
    hasil = []

    for nomor, data in enumerate(data_burung, start=1):
        sudut, kecepatan_awal, tinggi_pohon = data
        burung = Manuk(sudut, kecepatan_awal, tinggi_pohon)

        hasil.append({
            "nomor": nomor,
            "status": burung.status_tabrakan(),
            "ketinggian": burung.ketinggian_maksimum(),
        })

    return hasil
