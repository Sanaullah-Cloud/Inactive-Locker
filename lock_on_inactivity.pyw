import ctypes
import time
import sys

# Windows API functions
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# GetLastInputInfo ke liye structure
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]

def get_idle_time():
    """Return idle time in seconds"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    user32.GetLastInputInfo(ctypes.byref(lii))
    tick = kernel32.GetTickCount()
    return (tick - lii.dwTime) / 1000.0

def lock_workstation():
    """Lock the workstation (Windows + L)"""
    user32.LockWorkStation()

def main():
    print("Inactivity locker started. System will lock after 10 seconds of idle.")
    print("Press Ctrl+C to exit.")
    try:
        while True:
            idle_secs = get_idle_time()
            if idle_secs >= 10:
                print(f"Idle for {idle_secs:.1f} seconds. Locking now...")
                lock_workstation()
                # After lock, reset loop. But user will be at login screen.
                # Thodi der wait karein taaki multiple lock na ho.
                time.sleep(2)
            else:
                # Har 0.5 second mein check karein (CPU load kam rakhne ke liye)
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting inactivity locker.")
        sys.exit(0)

if __name__ == "__main__":
    main()