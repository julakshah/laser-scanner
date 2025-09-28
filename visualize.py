import serial
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd


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

                if serial_data == "scan done":
                    self.scanning_flag = False
                    break
                if serial_data != "":
                    line_data = serial_data.split()
                    csvwriter.writerow([line_data[0], line_data[1], line_data[2]])


def calibrate_data(csv_path="scanner_data.csv"):
    """converts data from analog voltage readings to distance in meters

    Constants:
        REF_VOLT = the voltage range of the laser signal pin in volts"""
    REF_VOLT = 5  # voltage
    with open(csv_path, "r", newline="") as raw_data:
        reader = csv.reader(raw_data, delimiter=",")
        with open("calibrated_scanner_data.csv", "w", newline="") as calib_data:
            writer = csv.writer(calib_data, delimiter=",")
            for row in reader:
                scan_v = (int(row[0]) / 1024) * REF_VOLT
                if scan_v != 0:
                    y = 23.3 / scan_v
                    writer.writerow([y, row[1], row[2]])


def flatten_data(csv_path="calibrated_scanner_data.csv"):
    """converts to data from polar to cartesian coordinates in inches"""

    REF_VOLT = 5  # voltage
    with open(csv_path, "r", newline="") as calib_data:
        reader = csv.reader(calib_data, delimiter=",")
        with open("cartesian_scanner_data.csv", "w", newline="") as cart_data:
            writer = csv.writer(cart_data, delimiter=",")
            writer.writerow(["x", "y", "z"])
            for row in reader:
                dist = float(row[0])
                top_ang = (int(row[1]) / 360) * 2 * np.pi  # convert toppos to rad
                bot_ang = (int(row[2]) / 360) * 2 * np.pi  # convert botpos to rad
                x = -1 * dist * float(np.cos(top_ang)) * float(np.sin(bot_ang))
                y = dist * float(np.cos(top_ang)) * float(np.cos(bot_ang))
                z = -1 * dist * float(np.sin(top_ang))
                writer.writerow([x, y, z])


def calibration_plot():
    """plots a plot of the calibration data along with the equation fitted
    in excel"""
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


def error_plot():
    """plots a plot of the expected distance to the actual distance"""
    df = pd.read_csv("error_data.csv")
    plt.scatter(df["in"], df["voltage"], label="Measured Voltage")
    plt.scatter(df["in"], df["Expected Voltage"], label="Expected Voltage")
    plt.legend()
    plt.title("Error Between Measured and Expected Distance")
    plt.xlabel("Actual Distance (in.)")
    plt.ylabel("Measured Voltage Out (V)")
    plt.axes([0, 60, 0, 3])
    plt.savefig("error.png")


def scan_2d_plot():
    """plots a 2d representation of the scan"""
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    data = pd.read_csv("cartesian_scanner_data.csv")
    ax.scatter(
        data["x"],
        data["y"],
        data["z"],
        c=data["x"] ** 2 + data["z"] ** 2 + data["y"] ** 2,
        cmap="plasma",
    )
    ax.set_xlabel("x pos (in)")
    ax.set_ylabel("y pos (in)")
    ax.set_zlabel("z pos (in)")
    ax.axis("square")
    plt.savefig("2d_image.png")
    plt.show()


def main():
    """runs to program in it's entirety"""
    minion = scanMan("/dev/cu.usbmodemB43A4536DECC2")
    minion.begin_program()
    minion.write_data()
    # calibration_plot()
    error_plot()
    # calibrate_data()
    # flatten_data()
    # scan_2d_plot()


if __name__ == "__main__":
    main()
