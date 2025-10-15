# Data gejala awal (gejala ringan)
gejala_awal = {
    1: "Buang air besar (lebih dari 2 kali)",
    2: "Berak encer",
    3: "Berak berdarah",
    4: "Lesu dan tidak bergairah",
    5: "Tidak selera makan",
    6: "Mual dan sering muntah (lebih dari 1 kali)",
    7: "Sakit di bagian perut",
    8: "Tekanan darah rendah",
    9: "Pusing",
    10: "Pingsan",
    11: "Suhu badan tinggi",
    12: "Luka di bagian tertentu",
    13: "Tidak dapat menggerakkan anggota badan tertentu",
    14: "Pernah memakan sesuatu",
    15: "Memakan daging",
    16: "Memakan jamur",
    17: "Memakan makanan kaleng",
    18: "Membeli susu",
    19: "Meminum susu"
}

# Data gejala menengah dan gejala penyusunnya
gejala_menengah = {
    20: {"nama": "Mencret", "gejala_penyusun": [1, 2, 4, 5]},
    21: {"nama": "Muntah", "gejala_penyusun": [4, 5, 6]},
    22: {"nama": "Sakit perut", "gejala_penyusun": [4, 7]},
    23: {"nama": "Darah rendah", "gejala_penyusun": [4, 8, 9]},
    24: {"nama": "Koma", "gejala_penyusun": [8, 10]},
    25: {"nama": "Demam", "gejala_penyusun": [4, 5, 9, 11]},
    26: {"nama": "Septicaemia", "gejala_penyusun": [4, 8, 11, 12]},
    27: {"nama": "Lumpuh", "gejala_penyusun": [4, 13]},
    28: {"nama": "Mencret berdarah", "gejala_penyusun": [1, 2, 3, 4, 5]},
    29: {"nama": "Makan daging", "gejala_penyusun": [14, 15]},
    30: {"nama": "Makan jamur", "gejala_penyusun": [14, 16]},
    31: {"nama": "Makan makanan kaleng", "gejala_penyusun": [14, 17]},
    32: {"nama": "Minum susu", "gejala_penyusun": [18, 19]}
}

# Data diagnosis dan gejala menengah terkait
diagnosis = {
    33: {"nama": "Keracunan Staphylococcus aureus", "gejala_terkait": [20, 21, 22, 23, 29]},
    34: {"nama": "Keracunan jamur beracun", "gejala_terkait": [20, 21, 22, 24, 30]},
    35: {"nama": "Keracunan Salmonellae", "gejala_terkait": [20, 21, 22, 25, 26, 29]},
    36: {"nama": "Keracunan Clostridium botulinum", "gejala_terkait": [21, 27, 31]},
    37: {"nama": "Keracunan Campylobacter", "gejala_terkait": [28, 22, 25, 32]}
}

def hitung_nilai_gejala_menengah(jawaban_user):
    nilai_gejala_menengah = {}
    for kode, gm in gejala_menengah.items():
        gejala_penyusun = gm["gejala_penyusun"]
        total_gejala = len(gejala_penyusun)
        gejala_aktif = sum(jawaban_user.get(g, 0) for g in gejala_penyusun)
        if total_gejala > 0:
            nilai = (gejala_aktif / total_gejala) * 100
            nilai_gejala_menengah[kode] = nilai
    return nilai_gejala_menengah

def hitung_diagnosis(nilai_gejala_menengah):
    hasil_diagnosis = {}
    for kode, diag in diagnosis.items():
        gejala_terkait = diag["gejala_terkait"]
        total_gejala = len(gejala_terkait)
        if total_gejala == 0:
            continue
        total_nilai = sum(nilai_gejala_menengah.get(g, 0) for g in gejala_terkait)
        nilai_diagnosis = (1 / total_gejala) * total_nilai
        hasil_diagnosis[kode] = nilai_diagnosis
    return hasil_diagnosis

# ============= TAMPILAN UTAMA =============
import streamlit as st
st.title("SISTEM PAKAR DIAGNOSIS INFEKSI GASTRO USUS")

# Kolom layout: Sidebar untuk input + Main area untuk hasil
with st.sidebar:
    st.header("📋 Input Gejala")
    threshold = st.slider("Threshold Diagnosis (%)", min_value=0, max_value=100, value=80)
    st.caption("Centang semua gejala yang dirasakan untuk mendapatkan hasil diagnosis.")
    jawaban = {}
    for kode, gejala in gejala_awal.items():
        jawaban[kode] = st.checkbox(f"{kode}. {gejala}", key=f"gejala_{kode}")

if st.button("🔍 Lakukan Diagnosa", type="primary"):
    jawaban_user = {k: 1 if v else 0 for k, v in jawaban.items()}
    nilai_gejala = hitung_nilai_gejala_menengah(jawaban_user)
    hasil_diagnosis = hitung_diagnosis(nilai_gejala)

    st.header("📊 Hasil Diagnosis")

    # Gejala menengah
    with st.expander("🔍 Detail Gejala Menengah"):
        for kode, nilai in nilai_gejala.items():
            st.progress(nilai/100, text=f"{gejala_menengah[kode]['nama']}: {nilai:.1f}%")

    # Diagnosis utama
    st.subheader("🎯 Diagnosis Utama")
    if hasil_diagnosis:
        kode_tertinggi = max(hasil_diagnosis, key=hasil_diagnosis.get)
        nilai_tertinggi = hasil_diagnosis[kode_tertinggi]
        nama_diagnosis = diagnosis[kode_tertinggi]['nama']

        # Versi label terpisah
        st.markdown("**Kemungkinan Tertinggi:**")
        st.progress(nilai_tertinggi / 100)
        st.metric(
            label="Kemungkinan",
            value=f"{nilai_tertinggi:.1f}%",
            delta=f"Threshold: {threshold}%",
            delta_color="normal" if nilai_tertinggi >= threshold else "inverse"
        )

        if nilai_tertinggi >= threshold:
            st.success(f"**Kesimpulan:** {nama_diagnosis}")
        else:
            st.warning(f"**Kemungkinan**: {nama_diagnosis} (di bawah threshold)")

        # Semua diagnosis
        st.subheader("📈 Semua Hasil")
        for kode, nilai in sorted(hasil_diagnosis.items(), key=lambda x: x[1], reverse=True):
            status = "✅" if nilai >= threshold else "⚠️"
            st.write(f"{status} **{nilai:.1f}%** - {diagnosis[kode]['nama']}")
    else:
        st.error("Tidak ada diagnosis yang dapat ditentukan berdasarkan gejala yang dipilih.")
