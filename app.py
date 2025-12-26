import streamlit as st
import os
import shutil

CLASS_FOLDER_ROOT = r'Data\Frames_Categories'

image_folder = "Data/Screenshots"
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpeg')]


if 'image_index' not in st.session_state:
    st.session_state.image_index = 0
#Initialize the index in session state if it doesn't exist

def next_image():
    if st.session_state.image_index < len(image_files) - 1:
        st.session_state.image_index += 1
    else:
        st.session_state.image_index = 0  

def prev_image():
    if st.session_state.image_index > 0:
        st.session_state.image_index -= 1
    else:
        st.session_state.image_index = len(image_files) - 1  

def move_and_delete_image(img_path, img_dest_folder):
    if not os.path.isdir(img_dest_folder):
        print("Destination class folder doesn't exist - creating it")
        os.makedirs(img_dest_folder)

    print(f'Moving {img_path} to {img_dest_folder}')
    print("move_and_delete_image")
    shutil.copy(img_path, img_dest_folder)
    os.remove(img_path)
#Define auxiliary navigation functions   

def select_class():
    image_class = st.selectbox(
        "Select class", 
        os.listdir(CLASS_FOLDER_ROOT),
        index=None,
        placeholder="Select or type a new option...",
        accept_new_options=True,
        on_change=None
    )
    
    return image_class


#UI
st.title("Image Iterator")

if image_files:
    current_img_path = os.path.join(image_folder, image_files[st.session_state.image_index])
    st.image(current_img_path, caption=f"Showing: {image_files[st.session_state.image_index]}")
    #Display the current image

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.button("Prev", on_click=prev_image)
    with col2:
        st.button("Next", on_click=next_image)
    with col3:
        image_class = select_class()
    with col4:
        if image_class:
            destination_path = os.path.join(CLASS_FOLDER_ROOT, image_class)
            st.button("Confirm", on_click=move_and_delete_image, args=[current_img_path, destination_path])
    st.write(f"Image {st.session_state.image_index + 1} of {len(image_files)}")
    st.write(f"Choosing image {current_img_path}")
else:
    st.warning("No images found in the specified folder.")
