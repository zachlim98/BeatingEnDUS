# Import the client
from td.client import TDClient

# Create a new session, credentials path is optional.
TDSession = TDClient(
    client_id='DRSMU4TL964FO3QNBQHVL78X9SUPGGIL',
    redirect_uri='http://localhost',
    credentials_path='QM+2vPr7gFY4/k2F+eHMUFp1NKYdvy7VBPy1ytQUdTONCXiPj1S2e3cTFE9CMCTGeZganoC/1heqUeLoefJJpgIVEKuDd6rZRQBHrs1SqJg6C85XOzzNWmxMz6jThDn+AVvHkYNLYTe83rLgf8+FhbhqnEgTFIu2qfWed5H2RCjwFffbBlGsknSHYVtZ79P4bTR5b1bM/mHUb4H3ytWcEX54BdkaTQVhYgSUbFyCq0qkzThiaOPj7z65OaNQgrxgcBkhqFhqjjj8r8LIqvvUs6Vx8W+O/rs2859S8p5UHpvsGoUzxt/BozPiepz8EZS1+ktgtWVEWJEulWw8nmH+1CzfDJMei+0jW4nB43mgrRfWwG0elfNfIX3zwD1549KOIbo/R5UZ/XPUvTmX9ba8tgtBdcRduzZ0GRFaL5BWcI++UUPdsrp9++HKEhVxhqIkCZnz6ltKWYzJA4BUZLrbQecnLTvBBFMfcV7OL9VVK2ehpAgRS100MQuG4LYrgoVi/JHHvl7algtWvghYSOu88vLXay6Car/+9wRIwejGAB/ifu1qpY/U6VkjXWwgD3tb2y3xNhJMsr7FiwaMHA8Jxoet3cLbF1QzbBnZTS1AjpQPH6iZsi9k9XkJwY81vO6ME++CulfGc3k2Ke3uam8ppNf/JeloKM+9uJ6qAtQtbRmRpubkSIO7pvf9FvKIa3I6GZeEVAAUYPwRbeJkdXtdf8C2D7EG/Kz301gtiYqDw1W/wvzJJe7kHl3LU3EahAv7GHYLpZG/MXmkc1tOdqj++cqP2je0kR2CQ+owfLk5yYr4HF6Q4rugmvMfQ/2E1OeRk2ryYEXRRzmvbU4V81MOc4YDBhniGZ4wF8pN47HbAfeahqnsIsVGO0f0sgqBZABzb0frUj/wtHkZeZtXlKOUldf/iXlq+0ht3tu+GCqrU9gNL+XF8/oIHJgOXe5juYNva4NNWAorN5r1iVJKS/kuWgBxdzlPVm+xZs2wdRri1KKYguEi7B6z4Q==212FD3x19z9sWBHDJACbC00B75E'
)

# Login to the session
TDSession.login()

# Grab real-time quotes for 'MSFT' (Microsoft)
msft_quotes = TDSession.get_quotes(instruments=['MSFT'])

# Grab real-time quotes for 'AMZN' (Amazon) and 'SQ' (Square)
multiple_quotes = TDSession.get_quotes(instruments=['AMZN','SQ'])