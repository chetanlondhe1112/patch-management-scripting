import win32service
import win32serviceutil
import win32event
import servicemanager


class SimpleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SimpleService"
    _svc_display_name_ = "Simple Service"
    _svc_description_ = "A simple Windows service written in Python"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        import time
        while True:
            # Simulate some work
            with open("C:\\Logs\\SimpleService.log", "a") as f:
                f.write("Service is running...\n")
            time.sleep(5)  # Sleep for 5 seconds


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SimpleService)