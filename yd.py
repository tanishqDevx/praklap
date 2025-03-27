import sys
import time
import ydlidar

def run_lidar():
    # Initialize the LiDAR
    lidar = ydlidar.YDLidar()  # Use YDLidar instead of YDLidarX4
    lidar.setlidaropt(ydlidar.LidarPropSerialPort, "/dev/ttyUSB0")  # Update with your port
    lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
    lidar.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    lidar.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    lidar.setlidaropt(ydlidar.LidarPropSampleRate, 3)
    lidar.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
    lidar.setlidaropt(ydlidar.LidarPropSingleChannel, True)

    if not lidar.initialize():
        print("Failed to initialize LiDAR.")
        sys.exit(1)

    if not lidar.turnOn():
        print("Failed to turn on LiDAR.")
        sys.exit(1)

    try:
        print("Starting LiDAR scan...")
        while True:
            scan = lidar.doProcessSimple()
            if scan:
                for point in scan.points:
                    print(f"Angle: {point.angle:.2f}°, Distance: {point.distance:.2f}m")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping LiDAR...")
    finally:
        lidar.turnOff()
        lidar.disconnect()

if __name__ == "__main__":
    run_lidar()
