import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

# Change this to match your serial port
PORT_NAME = '/dev/ttyUSB0'  # Linux/macOS
# PORT_NAME = 'COM3'  # Windows

lidar = RPLidar(PORT_NAME)

def update_scan(lidar):
    """Retrieve and process LIDAR data"""
    for scan in lidar.iter_scans():
        angles = np.radians([point[1] for point in scan])  # Convert to radians
        distances = np.array([point[2] for point in scan])  # Distances in mm

        # Convert to Cartesian coordinates
        x = distances * np.cos(angles)
        y = distances * np.sin(angles)

        plt.clf()
        plt.scatter(x, y, s=2, c='b', alpha=0.6)
        plt.xlim(-4000, 4000)  # Adjust limits as needed
        plt.ylim(-4000, 4000)
        plt.xlabel("X (mm)")
        plt.ylabel("Y (mm)")
        plt.title("RPLIDAR A1 2D Scan")
        plt.grid(True)
        plt.pause(0.01)  # Pause for real-time update

try:
    plt.figure(figsize=(6, 6))
    update_scan(lidar)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()
