import os
import secrets
from fastapi import FastAPI, Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi.responses import JSONResponse

# Create the FastAPI app
app = FastAPI()

# Load environment variables
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
SECRET_KEY = os.environ.get('SECRET_KEY') or None

if None in (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY):
    raise BaseException('Missing env variables')

# Configure OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile','redirect_url': 'https://fastapi-auth-tcoyalueuq-uc.a.run.app/auth'},
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)



# Login route
@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Auth route
@app.route('/auth')
async def auth(request: Request):
    
    try:
        token = await oauth.google.authorize_access_token(request)
        # user_data = await oauth.google.parse_id_token(request, token)
        # Clear the stored state after successful authorization  
    except OAuthError as e:
        # Handle OAuth errors
        print("OAuthError:", e)
        return RedirectResponse(url='/login')  # Redirect to login page or handle error as needed
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')

# Public route
@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return f'Hello {name}! <a href="/logout">Logout</a>'
    return '<a href="/login">Login with Google</a>'

@app.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')
