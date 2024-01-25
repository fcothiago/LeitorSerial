import serial 
import threading
from threading import Thread
import time

class MonitorSerial(threading.Thread):
    def __init__(self, port, boudrate, timeout = 0.1, msg="", period = 0.8):
        super(MonitorSerial, self).__init__()
        self.tx_callback   , self.rx_callback   = lambda response : print(f'tx {response[0]} - { response[1] }')   , lambda response : print(f'rx {response[0]} - { response[1] }')
        self.flagStop, self.timeout, self.msg, self.period, self.port, self.boudrate   = True, timeout, msg, period,  port , boudrate

    def __tx_routine__(self):
        try:
            while self.flagStop:
                if self.msg:
                    data =   bytes.fromhex(self.msg)
                    self.__serial_port__.write(  data )
                    self.tx_callback((time.time()," ".join([str(hex(b))[2:] for b in data] )))
                time.sleep(self.period)
        except Exception as e:
            print(f"{e}")
        pass

    def __rx_routine__(self):
        try:
            buffer , timeref = [] , time.time()
            while self.flagStop:
                byte = self.__serial_port__.read(1)
                if byte:
                    buffer.append(byte)
                else:
                    self.rx_callback((timeref," ".join([ str(b)[4:6] for b in buffer])))
                    buffer , timeref = [] , time.time()
        except KeyboardInterrupt:
            exit()

    def run(self):
        rx_thread = threading.Thread(target=self.__rx_routine__,daemon=True)
        tx_thread = threading.Thread(target=self.__tx_routine__,daemon=True)
        try:
            self.__serial_port__ = serial.Serial(self.port, self.boudrate, timeout=self.timeout)
            rx_thread.start()
            tx_thread.start()
            rx_thread.join()
            tx_thread.join()
            self.__serial_port__.close()
        except Exception as e:
            print(f"Error Starting Serial {e}")

    def stop(self):
        self.flagStop = False


