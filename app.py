import vaccine_cvs
import vaccine_walgreen
import vaccine_safeway
import schedule
import time
from threading import Thread

def csv_tracking():
    schedule.every(30).minutes.do(vaccine_cvs.vaccine_tracking())

def walgreen_tracking():
    schedule.every(30).minutes.do(vaccine_walgreen.vaccine_tracking())
        
def safeway_tracking():
    schedule.every(30).minutes.do(vaccine_safeway.vaccine_tracking())
 
    
def main():
    Thread(target = csv_tracking).start()
    Thread(target = walgreen_tracking).start()
    Thread(target = safeway_tracking).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
    
    
