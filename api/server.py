import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask,request,jsonify,session,url_for,redirect
from authlib.integrations.flask_client import OAuth
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel(os.environ['MODEL'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app=app,origins=os.environ['ORIGIN'])

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENTID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_kwargs={
        'scope': 'user:email',
    },
)



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
    

@app.route('/main')
def index():
    if 'token' in session:
        user = github.get('user')
        return jsonify(user.json())
    return redirect(url_for('login'))

@app.route('/login')
def login():
    redirect_uri = 'http://localhost:3000/main'
    return github.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/auth/github/callback')
def authorize():
    token = github.authorize_access_token()
    if token is None:
        return redirect(url_for('login'))

    resp = github.get('https://api.github.com/user', token=token)
    user_info = resp.json()
    session['user'] = user_info
    session['token'] = token
    return redirect(f'http://localhost:3000/main?token={token["access_token"]}')


if __name__=='__main__':
    app.run('localhost',os.environ['PORT'])