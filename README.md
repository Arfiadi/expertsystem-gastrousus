# Sistem Pakar Diagnosis Infeksi Gastro Usus

Expert system untuk diagnosis infeksi saluran cerna (gastroenteritis) berbasis probabilitas. Aplikasi ini menganalisis gejala yang dilaporkan pengguna dan memberikan diagnosis bersama tingkat kepercayaan untuk lima jenis penyakit infeksi pencernaan.

**Live app:** https://arfiadi-expertsystem-gastrousus-diagnosis-gastrousus-pykpyh.streamlit.app/

## Penyakit yang Didiagnosis

Sistem dapat mendiagnosis:

1. **Keracunan Staphylococcus aureus** — infeksi bakteri dari makanan yang terkontaminasi
2. **Keracunan jamur beracun** — keracunan dari jamur yang tidak aman dikonsumsi
3. **Keracunan Salmonellae** — infeksi bakteri dari daging atau produk unggas
4. **Keracunan Clostridium botulinum** — keracunan dari makanan kaleng yang tidak steril
5. **Keracunan Campylobacter** — infeksi bakteri dari susu atau air yang terkontaminasi

## Cara Kerja

Sistem menggunakan **inference berbasis gejala berjenjang**:

1. **Gejala Awal (19 gejala)** — gejala dasar yang dilaporkan pasien (mencret, muntah, pusing, dll)
2. **Gejala Menengah (10 gejala)** — kombinasi dari gejala awal (misalnya "mencret" = gejala 1, 2, 4, 5)
3. **Diagnosis Akhir** — skor akhir dihitung dari rata-rata gejala menengah yang relevan dengan setiap penyakit

**Rumus skor diagnosis:**
- Setiap gejala menengah dinilai: `(jumlah gejala awal aktif / total gejala penyusun) × 100`
- Skor diagnosis: `(sum gejala menengah terkait) / jumlah gejala menengah) × 100`

Pengguna dapat mengatur **threshold diagnosis** untuk menentukan diagnosis dianggap valid atau hanya "kemungkinan".

## Setup & Jalankan

### Requirement
- Python 3.8+
- Streamlit 1.44.1+

### Instalasi

```bash
pip install -r requirements.txt
```

### Jalankan Aplikasi

```bash
streamlit run diagnosis_gastrousus.py
```

Buka browser ke `http://localhost:8501`

## Struktur Kode

```
diagnosis_gastrousus.py
  ├─ gejala_awal (dict)          → 19 gejala dasar
  ├─ gejala_menengah (dict)      → 10 gejala gabungan + komponennya
  ├─ diagnosis (dict)            → 5 penyakit + gejala menengah terkait
  ├─ hitung_nilai_gejala_menengah(jawaban_user)  → hitung skor gejala menengah
  ├─ hitung_diagnosis(nilai_gejala_menengah)     → hitung skor diagnosis akhir
  └─ UI Streamlit                → sidebar untuk input, main area untuk hasil
```

## Cara Penggunaan

1. Centang semua gejala yang sesuai pada sidebar kiri
2. Sesuaikan **Threshold Diagnosis** jika diperlukan (default: 80%)
3. Klik tombol **🔍 Lakukan Diagnosa**
4. Lihat hasil:
   - **Detail Gejala Menengah** — breakdown skor dari setiap gejala gabungan
   - **Diagnosis Utama** — diagnosis dengan probabilitas tertinggi
   - **Semua Hasil** — ranking semua 5 penyakit

Diagnosis dianggap **valid** (✅) jika skornya ≥ threshold, sebaliknya hanya "kemungkinan" (⚠️).

## Catatan Pengembangan

- Logika diagnosis **tidak menggunakan ML/neural network**, hanya rule-based inference
- Sistem diasumsikan data gejala sudah valid — tidak ada validasi khusus input
- Library pandas/numpy dikomentari di `requirements.txt` sebagai optional untuk ekspansi di masa depan
