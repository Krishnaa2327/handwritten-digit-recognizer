import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURATION ---
st.set_page_config(page_title="Digit Recognizer", layout="wide")

# --- MODEL LOADING ---
# Use caching to load the model only once
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('mnist_digit_recognizer.h5')
    return model

model = load_model()

# --- HEADER ---
st.title("✍️ Handwritten Digit Recognizer")
st.markdown("Draw a digit from 0 to 9 in the box below and click 'Predict' to see the model's guess.")

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Drawing Canvas")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 1)",  # Black background
        stroke_width=20,
        stroke_color="#FFFFFF",        # White stroke
        background_color="#000000",
        update_streamlit=True,
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
    )

with col2:
    st.subheader("Prediction")
    if st.button('Predict'):
        if canvas_result.image_data is not None:
            # Get the image data from the canvas
            img_data = canvas_result.image_data

            # Convert to a PIL Image
            pil_img = Image.fromarray(img_data.astype('uint8'), 'RGBA')

            # Convert to grayscale, resize, and process for the model
            img = pil_img.convert('L')
            img = img.resize((28, 28))
            img_array = np.array(img) / 255.0
            img_array = img_array.reshape(1, 28, 28, 1)

            # Make a prediction
            prediction = model.predict(img_array)
            predicted_digit = np.argmax(prediction)

            st.success(f"I'm guessing the digit is: **{predicted_digit}**")
            st.bar_chart(prediction[0])
        else:
            st.warning("Please draw a digit first.")