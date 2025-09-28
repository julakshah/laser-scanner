import serial
import matplotlib.pyplot as plt
import numpy as np
import csv


class scanMan:
    def __init__(self, port_string):
        self.arduino = self.get_arduino(port_string)
        self.scanning_flag = False

    def get_arduino(self, port_string):
        arduino = serial.Serial(port=port_string, baudrate=9600, timeout=1)
        return arduino

    def begin_program(self):
        self.scanning_flag = True
        self.arduino.write("run".encode("utf-8"))

    def write_data(self):
        """writes data taken from the serial port into a csv file"""
        with open("scanner_data.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            while self.scanning_flag:
                serial_data = self.arduino.readline().decode("utf-8")
                serial_data = serial_data.strip("b'")
                serial_data = serial_data.strip("\r\n'")

                print(serial_data)
                if serial_data == "scan done":
                    self.scanning_flag = False
                    break
                if serial_data != "":
                    line_data = serial_data.split()
                    csvwriter.writerow([line_data[0], line_data[1], line_data[2]])
        print("csv written")


def flatten_data(csv_path="~/Documents/GitHub/laser-scanner/scanner_data"):
    """converts to data from polar to cartesian coordinates"""
    print("flattening data")


def main():
    """runs to program in it's entirety"""
    minion = scanMan("/dev/cu.usbmodemB43A4536DECC2")
    minion.begin_program()
    minion.write_data()


if __name__ == "__main__":
    main()
