import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask,request,jsonify
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel(os.environ['MODEL'])

app = Flask(__name__)
CORS(app=app,origins=os.environ['ORIGIN'])

@app.route('/')
def test():
    return {'message':'This is a test route'}

@app.route('/gemini',methods=['POST'])
def gem():
    try:
        prompt = request.get_json()

        response = model.generate_content(prompt['message'])
        print()
        return jsonify({'response':response.candidates[0].content.parts[0].text}),200  
    except Exception as e:
        return jsonify({'error':f'error at line {e.__traceback__.tb_lineno}: {e}'}),400

if __name__=='__main__':
    app.run('localhost',os.environ['PORT'])