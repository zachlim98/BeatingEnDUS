# Import the client
from td.client import TDClient

# Create a new session, credentials path is optional.
TDSession = TDClient(
    client_id='DRSMU4TL964FO3QNBQHVL78X9SUPGGIL',
    redirect_uri='http://localhost',
    credentials_path='<PATH_TO_CREDENTIALS_FILE>'
)

# Login to the session
TDSession.login()

# Grab real-time quotes for 'MSFT' (Microsoft)
msft_quotes = TDSession.get_quotes(instruments=['MSFT'])

# Grab real-time quotes for 'AMZN' (Amazon) and 'SQ' (Square)
multiple_quotes = TDSession.get_quotes(instruments=['AMZN','SQ'])