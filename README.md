# 🎨 PIXORA — Web-Based Image Processing Editor
![Screenshot (280)](https://github.com/user-attachments/assets/c73f189c-c9b1-485f-ad9d-d5628eeb2cc4)

**PIXORA** adalah aplikasi pengolahan citra digital berbasis web yang dirancang untuk memberikan antarmuka interaktif dalam menerapkan berbagai transformasi dan filter gambar secara real-time.  
Proyek ini dibuat sebagai bagian dari tugas besar mata kuliah Pengolahan Citra Digital di **Universitas Jenderal Soedirman**.

---

## 🎯 Tujuan Aplikasi

- Memberikan alat bantu pembelajaran pengolahan citra berbasis antarmuka web interaktif.
- Menerapkan transformasi dasar citra secara real-time melalui browser.
- Mempermudah eksplorasi efek citra menggunakan tools visual yang mudah digunakan.

---

## 🧩 Fitur Utama

- **Home**: Halaman pembuka dan deskripsi aplikasi.
- **Effect**: Editor gambar dengan berbagai filter dan tools.
- **About**: Informasi tim pengembang dan detail proyek.

---

## 🖼️ Fitur Pengolahan Citra

- **Basic Filter**: Negative, Thresholding, Flip Horizontal, Rotate 90°.
- **Transformasi Ukuran**: Zoom In, Shrink.
- **Transformasi Warna**: Adjust Brightness, Contrast, Saturation.
- **Transformasi Spasial**: Sharpen, Log Transform, Translate, Reduce Noise.
- **Blending**: Gabungkan dua gambar dengan efek transparansi.

---

## ⚙️ Teknologi yang Digunakan

- **Bahasa**: Python  
- **Framework Web**: Streamlit  
- **Library**:
  - `OpenCV`: Proses transformasi dan filter citra
  - `NumPy`: Manipulasi matriks gambar
  - `Pillow (PIL)`: Pengolahan file gambar

---

## 🔧 Struktur File Utama

- `app.py`: Halaman utama Streamlit
- `utils/filters.py`: Kumpulan fungsi filter
- `assets/logo.png`: Logo aplikasi

---

## 🔄 Pipeline Preprocessing

1. **Konversi format**: PIL → NumPy (`np.array`)  
2. **Filter diterapkan**: Fungsi di `filters.py` (e.g. `cv2.cvtColor`, `cv2.filter2D`)  
3. **Konversi balik**: NumPy → PIL (`Image.fromarray`)  

---

## ✅ Hasil yang Dicapai

- Aplikasi web interaktif dan edukatif untuk pemula
- Antarmuka sederhana, mudah diakses tanpa instalasi rumit
- Memvisualisasikan efek transformasi citra secara langsung

---

## 🧑‍🎓 Tim Pengembang

- **Kintan Kinasih Mahaputri** (H1D022019)  
- **Mutia Nandhika** (H1D022078)  
- **Khansa Khalda** (H1D022086)

---

© 2025 – Fakultas Teknik – Informatika – Universitas Jenderal Soedirman
