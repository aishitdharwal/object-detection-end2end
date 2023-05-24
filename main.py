import boto3
import pandas as pd
import streamlit as st
import os
import io
import PIL.Image as Image

# s3 = boto3.client('s3')

# s3 = boto3.resource(
#     service_name='s3',
#     region_name='us-east-1',
#     aws_access_key_id='AKIAV6XGUBGYYFVAX7GL',
#     aws_secret_access_key='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'
# )

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# bucket = s3.Bucket(bucket_name)

# for obj in bucket.objects.all():
#     print(obj)

# obj = bucket.Object('best.pt').get()
# print(obj)
# print(obj['Body'])

@st.cache_data
def get_model():
    s3_client = boto3.client('s3',
        aws_access_key_id=st.secrets['aws_access_key_id'],
        aws_secret_access_key=st.secrets['aws_secret_access_key'],
        region_name=st.secrets['region_name'])
    
    bucket_name = 'object-detection-end2end'
    file_name = 'best.pt'
    s3_client.download_file(bucket_name, file_name, file_name)

get_model()
st.title('Object Detection App')

uploaded_file = st.file_uploader('Choose an image', type=['png','jpg','jpeg'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    uploaded_file_name = uploaded_file.name
    
    image = Image.open(io.BytesIO(bytes_data))
    
    image.save(uploaded_file_name)
    
    cmd = f"""python3 yolov7/detect.py --weights best.pt --conf 0.1 --source {uploaded_file_name} --view-img"""
    os.system(cmd)
    
    path = ''
    with open('path.txt', 'r') as file:
        path = file.read()
    
    print(path)
    path = path.replace('\\','/')
    print(path)
    image = Image.open(path)
    st.image(image)