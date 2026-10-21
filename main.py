
import sys

from subproblem import (
    subproblem_1,
    subproblem_2,
    subproblem_3,
    subproblem_4,
)


def baca_angka(prompt, tipe=float):
    return tipe(input(prompt))


def validasi_sudut(sudut):
    if not 0 <= sudut <= 90:
        raise ValueError("Sudut harus antara 0 dan 90.")


def validasi_kecepatan_dan_pohon(kecepatan, pohon=None):
    if kecepatan < 0:
        raise ValueError("Kecepatan tidak boleh negatif.")

    if pohon is not None and pohon < 0:
        raise ValueError("Tinggi pohon tidak boleh negatif.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"1", "2", "3", "4"}:
        print("Gunakan: python main.py [1|2|3|4]")
        return 1

    pilihan = sys.argv[1]

    try:
        if pilihan == "1":
            sudut = baca_angka("Sudut S (0-90): ", int)
            validasi_sudut(sudut)

            kecepatan = baca_angka("Kecepatan V: ")
            validasi_kecepatan_dan_pohon(kecepatan)

            jarak = subproblem_1(sudut, kecepatan)
            print(f"Hasil jarak: {jarak:.1f}")

        elif pilihan == "2":
            sudut = baca_angka("Sudut S (0-90): ", int)
            validasi_sudut(sudut)

            kecepatan = baca_angka("Kecepatan V: ")
            validasi_kecepatan_dan_pohon(kecepatan)

            waktu = subproblem_2(sudut, kecepatan)
            print(f"Waktu terbang: {waktu:.3f}")

        elif pilihan == "3":
            sudut = baca_angka("Sudut S (0-90): ", int)
            validasi_sudut(sudut)

            kecepatan = baca_angka("Kecepatan V: ")
            pohon = baca_angka("Tinggi pohon T: ")
            validasi_kecepatan_dan_pohon(kecepatan, pohon)

            status, tinggi = subproblem_3(
                sudut, kecepatan, pohon
            )
            print(f"Status : {status}")
            print(f"Ketinggian : {tinggi:.2f}")

        else:
            jumlah = baca_angka("Jumlah burung N: ", int)

            if jumlah < 1:
                raise ValueError("Jumlah burung minimal 1.")

            data_burung = []

            for i in range(1, jumlah + 1):
                print(f"\nData burung {i}:")

                sudut = baca_angka("Sudut S (0-90): ", int)
                validasi_sudut(sudut)

                kecepatan = baca_angka("Kecepatan V: ")
                pohon = baca_angka("Tinggi pohon T: ")
                validasi_kecepatan_dan_pohon(kecepatan, pohon)

                data_burung.append(
                    (sudut, kecepatan, pohon)
                )

            hasil = subproblem_4(data_burung)

            for burung in hasil:
                print(
                    f"Status Burung {burung['nomor']} : "
                    f"{burung['status']}"
                )
                print(f"Ketinggian: {burung['ketinggian']:.2f}")

    except (ValueError, OverflowError) as error:
        print(f"Input tidak valid: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
