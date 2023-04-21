Instructions For Running Product

All required packages can be installed with pip install -r requirements.txt

Running main.py file will launch the Flask website, which will be found (by default) at 127.0.0.1:5000

In order to utilize the trading functionality, the user will need to visit demo-futures.kraken.com/ and select 'Sign Up'. This will generate a new account, the credentials of which will be shown to the user. After this, the user will need to generate API keys in Settings>API Keys, where the user will need to create a new API key with full access. Following this, the user should transfer the funds on the account from the "Holding" wallet to the "Multi-Collateral Futures" wallet. This can be done by navigating to Wallets>Holding Wallets, selecting 'transfer' on both USD and BTC, and selecting the multi collateral futures wallet as the 'to' wallet. This will allow the program to access and utilize the funds for trading.

Following this, the user can sign up to the flask website utilizing their API keys.
