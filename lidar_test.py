import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rplidar import RPLidar
import time
import requests

# LIDAR Setup
PORT_NAME = '/dev/ttyUSB0'
MIN_DISTANCE = 500  # mm (Obstacle distance threshold)
SCAN_COUNT = 10000

# Rover Setup
ROVER_IP = '192.168.4.1'  # Update with your rover's IP

class RoverControl:
    def __init__(self, ip_address):
        self.ip = ip_address
        self.x, self.y = 0, 0  # Simulated hover position
        self.angle = 0  # Heading direction

    def send_command(self, motor, cmd, act):
        url = f'http://{self.ip}/js'
        payload = {"T": 10010, "id": motor, "cmd": cmd, "act": act}
        params = {"json": str(payload).replace("'", '"')}

        try:
            response = requests.get(url, params=params)
            print(f'Sent command to motor {motor}: cmd={cmd}, act={act}, response={response.status_code}')
        except Exception as e:
            print(f'Failed to send command: {e}')

    def move_forward(self, speed=10):
        self.send_command(1, speed, 3)
        self.send_command(2, -speed, 3)
        self.y += 100  # Simulated movement

    def move_backward(self, speed=10):
        self.send_command(1, -speed, 3)
        self.send_command(2, speed, 3)
        self.y -= 100  # Simulated movement

    def turn_left(self, speed=10):
        self.send_command(1, -speed, 3)
        self.send_command(2, -speed, 3)
        self.angle += 10  # Simulated turn

    def turn_right(self, speed=10):
        self.send_command(1, speed, 3)
        self.send_command(2, speed, 3)
        self.angle -= 10  # Simulated turn

    def stop(self):
        self.send_command(1, 0, 3)
        self.send_command(2, 0, 3)

def process_scan(scan):
    front_clear = True
    left_clear = True
    right_clear = True

    for (_, angle, distance) in scan:
        if distance == 0:
            continue
        if (angle >= 350 or angle <= 10) and distance < MIN_DISTANCE:
            front_clear = False
        elif 60 <= angle <= 120 and distance < MIN_DISTANCE:
            right_clear = False
        elif 240 <= angle <= 300 and distance < MIN_DISTANCE:
            left_clear = False

    print(f"Front clear: {front_clear}, Left clear: {left_clear}, Right clear: {right_clear}")
    return front_clear, left_clear, right_clear

def update_plot(scan, rover):
    plt.clf()

    # Process scan data
    angles = np.radians([point[1] for point in scan])
    distances = np.array([point[2] for point in scan])

    x = distances * np.cos(angles)
    y = distances * np.sin(angles)

    plt.scatter(x, y, s=2, c='b', alpha=0.6, label="LiDAR Data")

    # Draw hover position
    hover_patch = patches.Circle((rover.x, rover.y), 200, fc='r', alpha=0.5, label="Hover")
    plt.gca().add_patch(hover_patch)

    plt.xlim(-4000, 4000)
    plt.ylim(-4000, 4000)
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("RPLIDAR A1 2D Scan with Hover Position")
    plt.grid(True)
    plt.legend()
    plt.pause(0.01)

lidar = RPLidar(PORT_NAME)
rover = RoverControl(ROVER_IP)

try:
    print("Starting autonomous driving...")
    rover.stop()
    time.sleep(1)

    current_action = None

    for i, scan in enumerate(lidar.iter_scans()):
        print(f'Scan {i}: {len(scan)} measurements')

        front_clear, left_clear, right_clear = process_scan(scan)

        # Decision Logic
        if front_clear and current_action != 'forward':
            rover.move_forward(speed=20)
            current_action = 'forward'
            print("Moving forward...")

        elif not front_clear and left_clear and current_action != 'left':
            rover.turn_left(speed=20)
            current_action = 'left'
            print("Turning left...")

        elif not front_clear and right_clear and current_action != 'right':
            rover.turn_right(speed=20)
            current_action = 'right'
            print("Turning right...")

        elif not front_clear and not left_clear and not right_clear and current_action != 'reverse':
            rover.move_backward(speed=20)
            current_action = 'reverse'
            print("Reversing...")

        # Update plot
        update_plot(scan, rover)

        if i > SCAN_COUNT:
            print("Completed scan cycles. Stopping...")
            break

finally:
    print("Stopping LIDAR and Rover...")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    rover.stop()
