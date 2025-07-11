# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10AAf5w9zMtc4sgDdqYOj09XyjnNyigdD
"""
import streamlit as st
import os
import base64
from PIL import Image
from io import BufferedReader, BytesIO

from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()


#input
input_text = st.text_input("input")
create_num = st.sidebar.number_input("生成枚数",value = 1, step = 1)

#process
if st.button("go!"):
  #inputを英語に翻訳
  completion = client.chat.completions.create(
    model = "gpt-3.5-turbo", 
    temperature = 0,
    messages=[
        {"role":"system","content":"あなたはプロの翻訳家です。次の{文章}を英語に翻訳してください。"},
        {"role":"user","content":f'{input_text}'}
             ]
  )

  #翻訳されたpromptをもとに画像生成
  eng_prompt = completion.choices[0].message.content
  image = client.images.generate(
    model = 'dall-e-2',#or 'dall-e-3'
    prompt = eng_prompt,
    size = "512x512",
    n = create_num,
    style = "natural",
    quality = "standard",
    response_format="b64_json" #or "url"
  )

#output  
  #st.write(eng_prompt)
  uq_num = 1
  for item in image.data:
    img = base64.b64decode(item.b64_json)
    byte_img = BytesIO(img)
    img = Image.open(byte_img)
    st.image(img)

    BufferedReader_img = BufferedReader(byte_img)
    st.download_button(label = 'download',data = BufferedReader_img,
                        file_name = 'output.png',mime = "image/png",key = uq_num )

    uq_num += 1