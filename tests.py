import unittest
import subprocess
import sys
import time
import os

# Check if running in a headless environment e.g. running in Githubs CI/CD headless platform
running_headless = False

# Check for Linux headless environment
if sys.platform.startswith('linux'):
    # Check if the display manager service is running
    display_manager_status = subprocess.run(['systemctl', 'status', 'display-manager'], capture_output=True, text=True)
    if 'Active: active' not in display_manager_status.stdout:
        running_headless = True

# pyautogui requires a os.DISPLAY variable, so if it's a headless display it wont set that variable hence it will break script
if not running_headless:
    import pyautogui

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """
        CI/CD workflow triggers on pushing this repo to upstream on Github.
        Github actions will build binaries for Windows, MacOS, and Linux and run below command which
        checks for GUI and runs auto close tk window then returns result of pass 0 or fail 0.

        Bin built with: pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=. Heroes3MapLiker.py

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        if sys.platform == 'win32' and not running_headless:  # Check if running on Windows
            binary_path = 'Heroes3MapLiker.exe'
        elif sys.platform == 'darwin' and not running_headless:  # Check if running on macOS
            binary_path = './Heroes3MapLiker'
        elif sys.platform.startswith('linux') and not running_headless:  # Check if running on Linux and not headless
            binary_path = './Heroes3MapLiker'
        else:
            self.skipTest("Skipping test in headless environment")
            return

        # Start the binary
        process = subprocess.Popen([binary_path])

        # Wait a few seconds to ensure the GUI is fully loaded
        time.sleep(5)

        # Close the GUI application using pyautogui
        if sys.platform == 'win32':
            pyautogui.hotkey('alt', 'f4')  # On Windows
        elif sys.platform == 'darwin':
            pyautogui.hotkey('command', 'q')  # On macOS
        elif sys.platform.startswith('linux'):
            pyautogui.hotkey('alt', 'f4')  # On Linux (may vary depending on the window manager)

        # Wait for the process to terminate
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

        # Check if the binary executed successfully (exit code 0)
        self.assertEqual(process.returncode, 0)

if __name__ == '__main__':
    unittest.main()
