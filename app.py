
import streamlit as st
st.set_page_config(page_title="PIXORA", layout="centered")

import numpy as np
import cv2
from PIL import Image
from utils import filters
from io import BytesIO

if 'page' not in st.session_state:
    st.session_state['page'] = "🏠 Home"

menu_options = ["🏠 Home", "✨ Effect", "ℹ️ About"]
page = st.sidebar.selectbox("Navigasi", menu_options, index=menu_options.index(st.session_state['page']))
st.session_state['page'] = page

def pil_to_cv(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def cv_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

if page == "🏠 Home":
    st.title("📷 Selamat Datang di PIXORA")
    st.markdown("""
        ### Aplikasi Pengolahan Citra Digital
        Selamat datang di PIXORA, editor gambar interaktif untuk menerapkan berbagai efek citra secara real-time.
        Gunakan menu di sebelah kiri untuk mulai menjelajah fitur kami!
    """)
    st.image("assets/logo.png", width=200)
    if st.button("🚀 Mulai Mengedit!"):
        st.session_state['page'] = "✨ Effect"
        st.rerun()

elif page == "✨ Effect":
    st.title("🎨 Editor Gambar - PIXORA")

    if "original_image" not in st.session_state:
        st.session_state.original_image = None
        st.session_state.processed_image = None

    uploaded_file = st.file_uploader("📤 Upload gambar", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.session_state.original_image = image
        st.session_state.processed_image = image.copy()

    if st.session_state.processed_image:
        st.subheader("Pilih Filter")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("Negative"):
                st.session_state.processed_image = cv_to_pil(filters.image_negative(pil_to_cv(st.session_state.processed_image)))
            if st.button("Thresholding"):
                st.session_state.processed_image = cv_to_pil(filters.image_thresholding(pil_to_cv(st.session_state.processed_image)))

        with col2:
            if st.button("Rotate 90°"):
                st.session_state.processed_image = cv_to_pil(filters.image_rotating(pil_to_cv(st.session_state.processed_image), 90))
            if st.button("Flip Horizontal"):
                st.session_state.processed_image = cv_to_pil(filters.image_flipping(pil_to_cv(st.session_state.processed_image), "horizontal"))

        with col3:
            if st.button("Zoom In"):
                st.session_state.processed_image = cv_to_pil(filters.image_zooming(pil_to_cv(st.session_state.processed_image), 1.5))
            if st.button("Shrink"):
                st.session_state.processed_image = cv_to_pil(filters.image_shrinking(pil_to_cv(st.session_state.processed_image), 0.5))

        with col4:
            if st.button("Log Transform"):
                st.session_state.processed_image = cv_to_pil(filters.image_logarithmic(pil_to_cv(st.session_state.processed_image)))
            if st.button("Translate"):
                st.session_state.processed_image = cv_to_pil(filters.image_translation(pil_to_cv(st.session_state.processed_image), 50, 50))

        with col5:
            if st.button("Sharpen"):
                st.session_state.processed_image = cv_to_pil(filters.sharpen_image(pil_to_cv(st.session_state.processed_image)))
            if st.button("Reduce Noise"):
                st.session_state.processed_image = cv_to_pil(filters.reduce_noise(pil_to_cv(st.session_state.processed_image)))

        # Penyesuaian tambahan di bawah filter
        st.subheader("Penyesuaian Tambahan")
        col_a1, col_a2, col_a3 = st.columns(3)

        with col_a1:
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
            if st.button("Apply Contrast"):
                st.session_state.processed_image = cv_to_pil(filters.adjust_contrast(pil_to_cv(st.session_state.processed_image), contrast))

        with col_a2:
            saturation = st.slider("Saturation", 0.5, 2.0, 1.0, 0.1)
            if st.button("Apply Saturation"):
                st.session_state.processed_image = cv_to_pil(filters.adjust_saturation(pil_to_cv(st.session_state.processed_image), saturation))

        with col_a3:
            second_file = st.file_uploader("Blending Img", key="blend")
            if st.button("Blending") and second_file:
                img2 = Image.open(second_file).convert("RGB")
                st.session_state.processed_image = cv_to_pil(
                    filters.image_blending(
                        pil_to_cv(st.session_state.processed_image),
                        pil_to_cv(img2),
                        alpha=0.5
                    )
                )

        st.subheader("Tampilan Gambar")
        col_before, col_after = st.columns(2)
        with col_before:
            st.image(st.session_state.original_image, caption="Before", width=250)
        with col_after:
            st.image(st.session_state.processed_image, caption="After", width=250)

        st.subheader("Aksi")
        if st.button("🔄 Reset Gambar"):
            st.session_state.processed_image = st.session_state.original_image.copy()
            st.rerun()

        buf = BytesIO()
        st.session_state.processed_image.save(buf, format="PNG")
        st.download_button(
            label="💾 Unduh Gambar",
            data=buf.getvalue(),
            file_name="hasil_pixora.png",
            mime="image/png"
        )

elif page == "ℹ️ About":
    st.title("ℹ️ Tentang PIXORA")
    st.image("assets/logo.png", width=150)
    st.markdown("""
    **PIXORA** adalah aplikasi pengolahan citra berbasis web yang dibuat oleh tim:

    - Mutia Nandhika  (H1D022078)
    - Khansa Khalda  (H1D022086)
    - Kintan Kinasih Mahaputri  (H1D022012)

    Proyek ini dikembangkan sebagai sarana eksplorasi dan pembelajaran tentang pemrosesan citra digital dengan tampilan antarmuka yang ramah pengguna.
    """)
