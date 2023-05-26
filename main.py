import io
import os

import boto3
import pandas as pd
import PIL.Image as Image
import streamlit as st


@st.cache_data
def get_model():
    s3_client = boto3.client('s3')
    bucket_name = 'object-detection-end2end'
    file_name = 'best.pt'
    s3_client.download_file(bucket_name, file_name, file_name)

if os.path.isfile('best.pt'):
    pass
else:
    get_model()
    
st.title('Object Detection App')

uploaded_file = st.file_uploader('Choose an image', type=['png','jpg','jpeg'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    uploaded_file_name = uploaded_file.name
    
    image = Image.open(io.BytesIO(bytes_data))
    
    image.save(uploaded_file_name)
    
    cmd = f"""python3 yolov7/detect.py --weights best.pt --conf 0.1 --source "{uploaded_file_name}" --view-img"""
    os.system(cmd)
    
    path = ''
    with open('path.txt', 'r') as file:
        path = file.read()
    
    print(path)
    path = path.replace('\\','/')
    print(path)
    image = Image.open(path)
    st.image(image)