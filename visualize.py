import serial
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

scanning_flag = False


class scanMan:
    def __init__(self):
        self.arduino = get_arduino()

    def get_arduino():
        try:
            arduino = serial.Serial(port="COM4", baudrate=9600, timeout=0.1)
        except SerialTimeoutException:
            print("connection to arduino couldn't be esetablished")
        return arduino

    def begin_program():
        arduino.write("run".encode("utf-8"))

    def write_data():
        """writes data taken from the serial port into a csv file"""
        with open("scanner_data.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            while scanning_flag:
                serial_data = arduino.readline()
                print(serial_data)


def plotting():
    x = np.linspace(8, 59, 600)
    y = 22 * np.power(x, -0.984)
    df = pd.read_csv("calibration_data.csv")
    plt.scatter(df["in"], df["voltage"], label="Calibration Data")
    plt.plot(x, y, label="Fit Curve (22x^-0.984)", color="red")
    plt.legend()
    plt.title("Measured Voltage Out vs Actual Distance")
    plt.xlabel("Actual Distance (in.)")
    plt.ylabel("Measured Voltage Out (V)")
    plt.axes([0, 60, 0, 3])
    plt.savefig("calibration.png")


def main():
    """runs to program in it's entirety"""
    plotting()
    # minion = scanMan()
    # begin_program()


if __name__ == "__main__":
    main()
