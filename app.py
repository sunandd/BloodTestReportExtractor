from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


#function to load Gemini pro vision
model=genai.GenerativeModel("gemini-pro-vision")


def get_gemini_responce(input,image,prompt):
    responce=model.generate_content([input,image[0],prompt])
    return responce.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue() #reading the file into bytes

        image_parts= [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("NO file uploaded")
    

#initialize streamlit app

st.set_page_config(page_title="LAB Test Extractor")

st.header("Gemini Extractor Application")
input=st.text_input("input prompt:", key="input")
uploaded_file=st.file_uploader("Chose an image file", type=['jpj', 'jpeg','png','pdf'])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_column_width=True)

submit=st.button("Tell me about this report")

input_prompt=""" you are  expert in analysing human blood test report according to the world health organisation and understand the problem in the report  to suggest what to do next """

#if submit 
if submit:
    image_data = input_image_setup(uploaded_file)
    responce=get_gemini_responce(input_prompt, image_data, input )
    st.subheader("Here is suggestion")
    st.write(responce)