from Monitor import MonitorSerial

class SerialGui(MonitorSerial):
    def __init__(self, port, boudrate, timeout = 0.1, msg="", period = 0.8):
        super(MonitorSerial, self).__init__(port, boudrate, timeout, msg, period)
        self.rx_callback = lambda data: self.rx_data(data)
        self.tx_callback = lambda data: self.tx_data(data)

    def rx_data(self, data):
        pass

    def tx_data(self, data):
        pass