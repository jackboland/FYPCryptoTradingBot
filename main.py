from website import create_app
from website.basebot import get_candle_close
import threading

app = create_app()

def botrun():
    get_candle_close(app)   

if __name__ == '__main__':
    t1 = threading.Thread(target=botrun)
    t1.start()
    app.run(debug=True)
