# File: serivce running log
import time
import datetime as dt

def main():

    while True:
        #Simulate some work
        with open("C://Logs//SimpleService2.txt", "a") as f:
        #with open("/chetan/patchmgt/test/patchservice/SimpleService.txt", "a") as f:
            f.write(f"{dt.datetime.now()} : Service is running...\n")
        time.sleep(3)  # Sleep for 5 seconds

if __name__ == "__main__":
    main()