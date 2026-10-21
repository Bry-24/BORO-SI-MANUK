import math
import pygame

from phy import (
    GRAVITASI,
    komponen_kecepatan,
    hitung_jarak,
    hitung_waktu,
    hitung_ketinggian_maksimum,
)

# ============================================================
# BORO SI MANUK v4 - Projectile Motion & Tree Collision Lab
# Kontrol:
#   SPACE = pause / lanjut
#   R     = reset animasi
#   ESC/X = tutup jendela
# ============================================================

LEBAR = 1280
TINGGI = 800
FPS = 60

PUTIH = (248, 250, 253)
NAVY = (25, 40, 65)
ABU = (105, 120, 140)
GRID = (222, 229, 238)
BIRU = (45, 115, 225)
MERAH = (215, 65, 65)
HIJAU = (35, 145, 85)
ORANYE = (235, 135, 35)
COKELAT = (130, 80, 45)
KUNING = (245, 190, 45)
PANEL = (235, 241, 249)


def hitung_tinggi_di_x(x, vx, vy):
    """Menghitung ketinggian lintasan pada posisi horizontal x."""
    if vx <= 1e-9 or x < 0:
        return None

    t = x / vx
    y = vy * t - 0.5 * GRAVITASI * t**2

    if t < 0 or t > (2 * vy / GRAVITASI if vy > 0 else 0):
        return None

    return max(0.0, y)


def hitung_jarak_aman(tinggi_pohon, vx, vy, tinggi_maks):
    """
    Jarak pada lintasan turun ketika burung mencapai tinggi puncak pohon.
    Ini adalah batas terakhir untuk melewati pohon setinggi tersebut dengan aman
    dalam model titik dan gerak parabola ideal.
    """
    if vx <= 1e-9 or tinggi_pohon < 0 or tinggi_pohon > tinggi_maks:
        return None

    diskriminan = vy**2 - 2 * GRAVITASI * tinggi_pohon
    if diskriminan < 0:
        return None

    waktu_turun = (vy + math.sqrt(max(0.0, diskriminan))) / GRAVITASI
    return vx * waktu_turun


def gambar_simulasi(sudut, kecepatan, tinggi_pohon, jarak_pohon):
    pygame.init()
    layar = pygame.display.set_mode((LEBAR, TINGGI))
    pygame.display.set_caption("BORO SI MANUK v4 - Physics Simulator")

    font_judul = pygame.font.Font(None, 38)
    font_subjudul = pygame.font.Font(None, 24)
    font_data = pygame.font.Font(None, 25)
    font_kecil = pygame.font.Font(None, 21)
    font_status = pygame.font.Font(None, 27)

    jarak = hitung_jarak(sudut, kecepatan)
    waktu = hitung_waktu(sudut, kecepatan)
    tinggi_maks = hitung_ketinggian_maksimum(sudut, kecepatan)
    vx, vy = komponen_kecepatan(sudut, kecepatan)

    # Status buku: apakah ketinggian maksimum mencapai tinggi pohon?
    status_buku = int(tinggi_maks >= tinggi_pohon)

    # Status pada posisi pohon.
    tinggi_di_pohon = hitung_tinggi_di_x(jarak_pohon, vx, vy)
    di_jangkauan = tinggi_di_pohon is not None and 0 <= jarak_pohon <= jarak
    if not di_jangkauan:
        tinggi_di_pohon = None
        selisih = None
        tabrakan = False
    else:
        selisih = tinggi_di_pohon - tinggi_pohon
        tabrakan = selisih <= 0
    jarak_aman = hitung_jarak_aman(
        tinggi_pohon, vx, vy, tinggi_maks
    )

    # Grafik kiri, panel kanan.
    kiri, kanan = 82, 785
    atas, bawah = 155, 675
    lebar_grafik = kanan - kiri
    tinggi_grafik = bawah - atas

    # Pastikan pohon dan lintasan terlihat, termasuk jika pohon di luar jangkauan.
    rentang_x = max(jarak, jarak_pohon, 1.0) * 1.10
    rentang_y = max(tinggi_maks, tinggi_pohon, 1.0) * 1.20
    skala_x = lebar_grafik / rentang_x
    skala_y = tinggi_grafik / rentang_y

    def ke_layar(x, y):
        return (
            int(kiri + x * skala_x),
            int(bawah - y * skala_y),
        )

    lintasan = []
    if waktu > 0:
        for i in range(301):
            t = waktu * i / 300
            x = vx * t
            y = max(0.0, vy * t - 0.5 * GRAVITASI * t**2)
            lintasan.append(ke_layar(x, y))
    else:
        lintasan = [ke_layar(0, 0)]

    puncak = ke_layar(jarak / 2, tinggi_maks)
    pangkal_pohon = ke_layar(jarak_pohon, 0)
    puncak_pohon = ke_layar(jarak_pohon, tinggi_pohon)
    titik_di_pohon = (
        ke_layar(jarak_pohon, tinggi_di_pohon)
        if tinggi_di_pohon is not None else None
    )
    titik_aman = (
        ke_layar(jarak_aman, tinggi_pohon)
        if jarak_aman is not None and jarak_aman <= rentang_x else None
    )

    waktu_simulasi = 0.0
    jam = pygame.time.Clock()
    berjalan = True
    jeda = False

    while berjalan:
        dt = jam.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                berjalan = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_x):
                    berjalan = False
                elif event.key == pygame.K_SPACE:
                    jeda = not jeda
                elif event.key == pygame.K_r:
                    waktu_simulasi = 0.0

        if not jeda and waktu > 0:
            waktu_simulasi += dt * waktu / 5.5
            if waktu_simulasi > waktu:
                waktu_simulasi = 0.0

        x_burung = vx * waktu_simulasi
        y_burung = max(
            0.0,
            vy * waktu_simulasi
            - 0.5 * GRAVITASI * waktu_simulasi**2,
        )
        posisi_burung = ke_layar(x_burung, y_burung)

        layar.fill(PUTIH)

        # Header.
        layar.blit(font_judul.render("BORO SI MANUK v4", True, NAVY), (35, 24))
        layar.blit(
            font_subjudul.render(
                "Simulasi gerak parabola, batas aman, dan deteksi tabrakan",
                True, ABU,
            ),
            (37, 65),
        )

        # Grid dan angka sumbu.
        for i in range(6):
            x_grid = kiri + i * lebar_grafik / 5
            pygame.draw.line(
                layar, GRID, (int(x_grid), atas), (int(x_grid), bawah), 1
            )
            nilai_x = rentang_x * i / 5
            label_x = font_kecil.render(f"{nilai_x:.0f}", True, ABU)
            layar.blit(
                label_x,
                (int(x_grid) - label_x.get_width() // 2, bawah + 8),
            )

            y_grid = bawah - i * tinggi_grafik / 5
            pygame.draw.line(
                layar, GRID, (kiri, int(y_grid)), (kanan, int(y_grid)), 1
            )
            nilai_y = rentang_y * i / 5
            label_y = font_kecil.render(f"{nilai_y:.0f}", True, ABU)
            layar.blit(label_y, (kiri - 53, int(y_grid) - 9))

        pygame.draw.line(layar, NAVY, (kiri, atas), (kiri, bawah), 2)
        pygame.draw.line(layar, NAVY, (kiri, bawah), (kanan, bawah), 2)

        layar.blit(
            font_kecil.render("Jarak horizontal X (m)", True, NAVY),
            (kiri + 225, bawah + 35),
        )
        layar.blit(
            font_kecil.render("Tinggi Y (m)", True, NAVY),
            (kiri - 60, atas - 25),
        )

        if not jeda and waktu > 0:
              waktu_simulasi += dt * waktu / 5.5
        if waktu_simulasi > waktu:
                waktu_simulasi = 0.0

        x_burung = vx * waktu_simulasi
        y_burung = max(
            0.0,
            vy * waktu_simulasi
            - 0.5 * GRAVITASI * waktu_simulasi**2,
        )
        posisi_burung = ke_layar(x_burung, y_burung)

        layar.fill(PUTIH)

        # Header.
        layar.blit(font_judul.render("BORO SI MANUK v4", True, NAVY), (35, 24))
        layar.blit(
            font_subjudul.render(
                "Simulasi gerak parabola, batas aman, dan deteksi tabrakan",
                True, ABU,
            ),
            (37, 65),
        )

        # Grid dan angka sumbu.
        for i in range(6):
            x_grid = kiri + i * lebar_grafik / 5
            pygame.draw.line(
                layar, GRID, (int(x_grid), atas), (int(x_grid), bawah), 1
            )
            nilai_x = rentang_x * i / 5
            label_x = font_kecil.render(f"{nilai_x:.0f}", True, ABU)
            layar.blit(
                label_x,
                (int(x_grid) - label_x.get_width() // 2, bawah + 8),
            )

            y_grid = bawah - i * tinggi_grafik / 5
            pygame.draw.line(
                layar, GRID, (kiri, int(y_grid)), (kanan, int(y_grid)), 1
            )
            nilai_y = rentang_y * i / 5
            label_y = font_kecil.render(f"{nilai_y:.0f}", True, ABU)
            layar.blit(label_y, (kiri - 53, int(y_grid) - 9))

        pygame.draw.line(layar, NAVY, (kiri, atas), (kiri, bawah), 2)
        pygame.draw.line(layar, NAVY, (kiri, bawah), (kanan, bawah), 2)

        layar.blit(
            font_kecil.render("Jarak horizontal X (m)", True, NAVY),
            (kiri + 225, bawah + 35),
        )
        layar.blit(
            font_kecil.render("Tinggi Y (m)", True, NAVY),
            (kiri - 60, atas - 25),
        )

        # Lintasan ideal.
        if len(lintasan) > 1:
            pygame.draw.lines(layar, BIRU, False, lintasan, 3)

        # Batas aman: titik pada lintasan turun saat y = tinggi pohon.
        if titik_aman is not None:
            pygame.draw.line(
                layar, HIJAU,
                (titik_aman[0], atas),
                (titik_aman[0], bawah),
                1,
            )
            pygame.draw.circle(layar, HIJAU, titik_aman, 6)
            layar.blit(
                font_kecil.render("BATAS AMAN", True, HIJAU),
                (min(titik_aman[0] + 8, kanan - 100), max(atas, titik_aman[1] - 25)),
            )

        # Garis penunjuk pohon.
        if 0 <= jarak_pohon <= rentang_x:
            pygame.draw.line(
                layar, (175, 190, 205),
                pangkal_pohon, (pangkal_pohon[0], atas), 1,
            )

        # Pohon: batang dan tajuk.
        pygame.draw.line(layar, COKELAT, pangkal_pohon, puncak_pohon, 8)
        px, py = puncak_pohon
        pygame.draw.polygon(
            layar, HIJAU,
            [(px, py - 16), (px - 20, py + 13), (px + 20, py + 13)],
        )
        layar.blit(
            font_kecil.render("POHON", True, HIJAU),
            (min(px + 12, kanan - 75), max(atas, py - 39)),
        )
        
         # Titik saat burung berada di posisi pohon.
        if titik_di_pohon is not None:
            warna_titik = MERAH if tabrakan else HIJAU
            pygame.draw.line(
                layar, warna_titik, titik_di_pohon, puncak_pohon, 2
            )
            pygame.draw.circle(layar, warna_titik, titik_di_pohon, 7)
            label = "TITIK TABRAKAN" if tabrakan else "TITIK LINTASAN"
            layar.blit(
                font_kecil.render(label, True, warna_titik),
                (max(kiri + 4, titik_di_pohon[0] - 95),
                 max(atas, titik_di_pohon[1] - 25)),
            )

        # Puncak parabola.
        pygame.draw.circle(layar, MERAH, puncak, 6)
        layar.blit(
            font_kecil.render("H max", True, MERAH),
            (puncak[0] + 9, max(atas, puncak[1] - 25)),
        )

        # Burung bergerak.
        pygame.draw.circle(layar, ORANYE, posisi_burung, 9)
        pygame.draw.circle(layar, NAVY, posisi_burung, 9, 1)

        # Panel kanan.
        panel_x = 820
        pygame.draw.line(layar, GRID, (800, 110), (800, 750), 2)
        layar.blit(font_judul.render("DATA SIMULASI", True, NAVY), (panel_x, 125))

        data = [
            f"Sudut: {sudut} derajat",
            f"Kecepatan awal: {kecepatan:.2f} m/s",
            f"Jarak maksimum: {jarak:.2f} m",
            f"Waktu terbang: {waktu:.3f} s",
            f"Tinggi maksimum: {tinggi_maks:.2f} m",
            f"Tinggi pohon: {tinggi_pohon:.2f} m",
            f"Jarak pohon: {jarak_pohon:.2f} m",
            f"Waktu animasi: {waktu_simulasi:.2f} s",
            f"Posisi burung X: {x_burung:.2f} m",
            f"Posisi burung Y: {y_burung:.2f} m",
        ]

        for i, teks in enumerate(data):
            layar.blit(
                font_data.render(teks, True, NAVY),
                (panel_x, 170 + i * 31),
            )
        # Status menurut buku.
        pygame.draw.rect(
            layar, PANEL, (panel_x, 490, 390, 42), border_radius=8
        )
        layar.blit(
            font_status.render(f"Status buku: {status_buku}", True, NAVY),
            (panel_x + 12, 498),
        )

        # Status tabrakan berdasarkan posisi.
        if tinggi_di_pohon is None:
            teks_status = "POHON DI LUAR LINTASAN"
            warna_status = ABU
        elif tabrakan:
            teks_status = "STATUS POSISI: TABRAKAN"
            warna_status = MERAH
        else:
            teks_status = "STATUS POSISI: AMAN"
            warna_status = HIJAU

        pygame.draw.rect(
            layar, (255, 255, 255),
            (panel_x, 540, 400, 43), border_radius=8,
        )
        layar.blit(
            font_status.render(teks_status, True, warna_status),
            (panel_x + 8, 548),
        )

        if tinggi_di_pohon is not None:
            layar.blit(
                font_kecil.render(
                    f"Tinggi di pohon: {tinggi_di_pohon:.2f} m",
                    True, NAVY,
                ),
                (panel_x, 597),
            )
            layar.blit(
                font_kecil.render(
                    f"Selisih dari puncak: {selisih:+.2f} m",
                    True, warna_status,
                ),
                (panel_x, 623),
            )
        else:
            layar.blit(
                font_kecil.render(
                    "Pohon berada di luar jangkauan lintasan.",
                    True, ABU,
                ),
                (panel_x, 597),
            )

        if jarak_aman is None:
            teks_aman = "Batas aman: tidak tersedia"
        else:
            teks_aman = f"Batas aman lintasan turun: X = {jarak_aman:.2f} m"

        layar.blit(font_kecil.render(teks_aman, True, HIJAU), (panel_x, 652))

        kontrol = "SPACE: pause/lanjut   R: reset   ESC/X: keluar"
        layar.blit(font_kecil.render(kontrol, True, ABU), (panel_x, 695))

        if jeda:
            layar.blit(
                font_status.render("SIMULASI DIJEDA", True, ORANYE),
                (panel_x, 724),
            )

        pygame.display.flip()

    pygame.quit()


def main():
    try:
        sudut = int(input("Sudut S (0-90): "))
        if not 0 <= sudut <= 90:
            raise ValueError("Sudut harus antara 0 dan 90.")

        kecepatan = float(input("Kecepatan V (m/s): "))
        if not math.isfinite(kecepatan) or kecepatan < 0:
            raise ValueError("Kecepatan harus finite dan tidak negatif.")

        tinggi_pohon = float(input("Tinggi pohon T (m): "))
        if not math.isfinite(tinggi_pohon) or tinggi_pohon < 0:
            raise ValueError("Tinggi pohon harus finite dan tidak negatif.")

        jarak_pohon = float(input("Jarak pohon dari peluncuran (m): "))
        if not math.isfinite(jarak_pohon) or jarak_pohon < 0:
            raise ValueError("Jarak pohon harus finite dan tidak negatif.")

        gambar_simulasi(sudut, kecepatan, tinggi_pohon, jarak_pohon)

    except (ValueError, OverflowError) as error:
        print(f"Input tidak valid: {error}")
    except pygame.error as error:
        print(f"Gagal membuka jendela Pygame: {error}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
