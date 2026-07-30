import schedule
import time

from run import run_pipeline


schedule.every(
    1
).hours.do(run_pipeline)


while True:

    schedule.run_pending()

    time.sleep(60)
