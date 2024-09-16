
import time
from datetime import datetime as dtime

# return current timestamp in nanoeconds
def timeNow():
    return int(time.time() * 1000 * 1000)