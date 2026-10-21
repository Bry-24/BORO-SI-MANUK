
"""
BORO SI MANUK
Module: phy.py
Fungsi: Mesin perhitungan fisika gerak parabola.
"""

import math

# Konstanta gravitasi (m/s^2)
GRAVITASI = 10.0


def komponen_kecepatan(sudut, kecepatan_awal):
    """
    Menghitung komponen horizontal dan vertikal
    dari kecepatan awal.

    Returns:
        tuple: (vx, vy) dalam m/s
    """
    sudut_rad = math.radians(sudut)

    vx = kecepatan_awal * math.cos(sudut_rad)
    vy = kecepatan_awal * math.sin(sudut_rad)

    return vx, vy


def hitung_jarak(sudut, kecepatan_awal):
    """
    Menghitung jarak horizontal ketika burung
    kembali ke ketinggian awal.

    Returns:
        float: jarak dalam meter
    """
    sudut_rad = math.radians(sudut)

    jarak = (
        kecepatan_awal**2
        * math.sin(2 * sudut_rad)
        / GRAVITASI
    )

    return jarak


def hitung_waktu(sudut, kecepatan_awal):
    """
    Menghitung waktu total penerbangan
    hingga kembali ke ketinggian awal.

    Returns:
        float: waktu dalam detik
    """
    _, vy = komponen_kecepatan(sudut, kecepatan_awal)

    waktu = (2 * vy) / GRAVITASI

    return waktu


def hitung_ketinggian_maksimum(sudut, kecepatan_awal):
    """
    Menghitung ketinggian maksimum relatif
    terhadap titik peluncuran.

    Returns:
        float: ketinggian dalam meter
    """
    _, vy = komponen_kecepatan(sudut, kecepatan_awal)

    tinggi = (vy**2) / (2 * GRAVITASI)

    return tinggi


def hitung_posisi(sudut, kecepatan_awal, waktu):
    """
    Menghitung posisi burung pada waktu tertentu.

    Returns:
        tuple: (x, y) dalam meter,
        relatif terhadap titik peluncuran.
    """
    vx, vy = komponen_kecepatan(sudut, kecepatan_awal)

    x = vx * waktu
    y = (vy * waktu) - (0.5 * GRAVITASI * waktu**2)

    return x, y
