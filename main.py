import streamlit as st
import h5py
import numpy as np

ROWS = 4
COLUMNS = 4
PAGE_SIZE = ROWS * COLUMNS

def rescale_array(arr):
    min_val = arr.min()
    max_val = arr.max()
    if min_val == max_val:
        return np.zeros_like(arr, dtype=np.uint8)
    rescaled_array = 255 * (arr - min_val) / (max_val - min_val)
    return rescaled_array.astype(np.uint8)

def draw_page(page, h5, slice_1, slice_2):
    i = PAGE_SIZE * (page - 1)
    for row in range(ROWS):
        columns = st.columns(COLUMNS)
        for c in columns:
            img_id = h5['ID'][i]
            img_data = h5['X_nii'][i]
            with c:
                st.write('ID: {}'.format(img_id))
                columns_lvl2 = st.columns(2)
                with columns_lvl2[0]:
                    st.image(rescale_array(img_data[:, :, slice_1]))
                with columns_lvl2[1]:
                    st.image(rescale_array(img_data[:, slice_2, :]))
            i += 1

css = """
    <style>
        .container-border, div[data-testid="column"] {
            border: 2px solid #000;
            padding: 3px;
        }
        div[data-testid="column"] div[data-testid="column"] {
            border: 0
        }
    </style>
"""

st.set_page_config(layout="wide")

st.markdown(css, unsafe_allow_html=True)

st.write('Visualizador de contenido de los .hdf5')
filepath = st.text_input("Ingresa el path al archivo .hdf5")

if filepath:
    h5 = h5py.File(filepath, "r")
    if h5:
        item_count = h5["X_nii"].len()
        total_pages = (item_count // PAGE_SIZE) + 1
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        slice_1 = st.number_input("Slice Index 1", min_value=0, max_value=h5['X_nii'].shape[2] - 1, value=h5['X_nii'].shape[2] // 2)
        slice_2 = st.number_input("Slice Index 2", min_value=0, max_value=h5['X_nii'].shape[1] - 1, value=h5['X_nii'].shape[1] // 2)
        
        st.write('Page {}/{}'.format(page, total_pages))
        
        draw_page(page, h5, slice_1, slice_2)