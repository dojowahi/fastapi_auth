import os
import secrets
from fastapi import FastAPI, Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

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
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Generate a random string for state parameter
def generate_state():
    return secrets.token_urlsafe(16)

# Login route
@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for our /auth endpoint
    # Generate a random state and store it in the session
    state = generate_state()
    request.session['oauth_state'] = state
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)

# Auth route
@app.route('/auth')
async def auth(request: Request):
    # Retrieve the stored state from the session
    stored_state = request.session.get('oauth_state')
    # Retrieve the state parameter returned by Google
    state = request.query_params.get('state')
    if stored_state is None or state != stored_state:
        # Handle mismatching state error
        print("Mismatching state error")
        return RedirectResponse(url='/login')
    
    try:
        token = await oauth.google.authorize_access_token(request)
        user_data = await oauth.google.parse_id_token(request, token)
        # Clear the stored state after successful authorization
        request.session.pop('oauth_state', None)
        # Store user data in session or handle as needed
        request.session['user'] = dict(user_data)
        return RedirectResponse(url='/')
    except OAuthError as e:
        # Handle OAuth errors
        print("OAuthError:", e)
        return RedirectResponse(url='/login')  # Redirect to login page or handle error as needed

# Public route
@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return f'Hello {name}! <a href="/logout">Logout</a>'
    return '<a href="/login">Login with Google</a>'
