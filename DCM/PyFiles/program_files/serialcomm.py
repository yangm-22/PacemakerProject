import serial
import glob
import sys
import struct
import time

class SerialCommunication:
    def __init__(self, port='/dev/tty.wlan-debug', baudrate=115200, timeout=0.02):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.packet_size = 26
        self.packet_format = ['B'] * self.packet_size

    def open_serial_connection(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_TWO,
                timeout=self.timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False,
                write_timeout=None,
                inter_byte_timeout=None
            )
        except serial.SerialException as e:
            pass

    def close_serial_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_packet(self, values):
        self.open_serial_connection()
        SYNC_BYTE = b"\x16\x55"
        packet = SYNC_BYTE 
        for format_specifier, value in zip(self.packet_format, values):
            packet += struct.pack(format_specifier, value)
        self.ser.write(packet)
        self.close_serial_connection()

    def receive_packet(self):
        # Close the serial connection if it's open
        if self.ser and self.ser.is_open:
            self.ser.close()

        # Open a new serial connection
        self.open_serial_connection()

        packet = b"\x16\x22" + b'\x00'*26
        self.ser.write(packet)
        data = self.ser.read(42)  # Read the required number of bytes

        new_format = self.packet_format.copy()
        new_format = new_format + ["d", "d"]

        self.values = struct.unpack('<' + ''.join(new_format), data)

        # Clear data and values before returning
        values_to_return = self.values[:26]
        self.values = None

        return values_to_return
    
    def get_egram_data(self):
        # Close the serial connection if it's open
        if self.ser and self.ser.is_open:
            self.ser.close()

        # Open a new serial connection
        self.open_serial_connection()

        packet = b"\x16\x22" + b'\x00'*26
        self.ser.write(packet)
        data = self.ser.read(42)  # Read the required number of bytes

        new_format = self.packet_format.copy()
        new_format = new_format + ["d", "d"]

        self.values = struct.unpack('<' + ''.join(new_format), data)

        # Clear data and values before returning
        values_to_return = self.values[26:]
        self.values = None

        return values_to_return

    
def list_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
