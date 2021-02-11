from datetime import datetime
from datetime import timedelta
from td.client import TDClient

# Create a new session
TDSession = TDClient(
    client_id='DRSMU4TL964FO3QNBQHVL78X9SUPGGIL',
    redirect_uri='http://localhost',
    credentials_path='X:/GitHub/beatingENd/BeatingEnDUS/Account Tracking/tdaAPI2/cred.json',
    auth_flow='flask'
)

# Login to the session
TDSession.login()