from website import create_app
from website.bots.basebot import get_candle_close
from flask_login import current_user
import threading

backtesting = 0
app = create_app()

def botrun():
    get_candle_close(app)   

if __name__ == '__main__':
    t1 = threading.Thread(target=botrun)
    t1.start()
    app.run(debug=True)
