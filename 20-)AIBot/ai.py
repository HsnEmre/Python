
from flask import Flask,render_template,request
import os 
import contextlib

#log kayitlarini bastirma
with open(os.devnull,'w') as devnull,contextlib.redirect_stderr__strderr(devnull):
    import google.generativeai as genai

app=Flask(__name__)    
#api anahtarini cagir

genai.configure(api_key="your api key")

generation_config={
    "tempature":1,
    "top_p":0.95,
    "top_k":40,
    "max_output_tokens":8192,
    "response_mine_type":"text/plain",
}

mode=genai.GenerativeModel(
    model_name="gemini=2.0-flash",
    generation_config=generation_config
)