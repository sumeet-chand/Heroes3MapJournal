import unittest
import subprocess
import sys
import time
import pyautogui
import os

def is_headless():
    """
    Check if running in a headless environment (e.g. GitHub CI/CD).
    On Linux: checks if display-manager is active.
    On macOS: checks if running under SSH or if DISPLAY variable is missing.
    On Windows: checks if running under SSH or if no interactive desktop session.

    Returns:
        True if running headless, False otherwise.
    """
    if sys.platform.startswith('linux'):
        display_manager_status = subprocess.run(
            ['systemctl', 'status', 'display-manager'],
            capture_output=True, text=True
        )
        if 'Active: active' not in display_manager_status.stdout:
            return True
        if not os.environ.get('DISPLAY'):
            return True
    elif sys.platform == 'darwin':
        # On macOS, check for SSH or missing DISPLAY
        if os.environ.get('SSH_CONNECTION'):
            return True
        if not os.environ.get('DISPLAY'):
            return True
    elif sys.platform == 'win32':
        # On Windows, check for SSH or if not running in an interactive session
        if os.environ.get('SSH_CONNECTION'):
            return True
        try:
            import ctypes
            user32 = ctypes.windll.user32
            if not user32.GetForegroundWindow():
                return True
        except Exception:
            return True
    return False

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """

        IMPORTANT: pyInstaller builds in /build but deploys binary in /dist

        Included GitHub Actions CI/CD workflow on pushes to  upstream repository in Github.
        will build binaries for Windows, MacOS, and Linux then run tests.py. Tests.py then
        checks non headless displays GUI and runs auto close tk window against the binaries
        to simulate a user running the executable in production. The output is a success code
        0 pass, and 1 failure.

        Bin built with: pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=. main.py

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        # Determine binary path based on platform
        if sys.platform == 'win32':
            binary_path = 'dist/Heroes3MapJournal.exe'
        elif sys.platform == 'darwin':
            binary_path = 'dist/Heroes3MapJournal-macos'
        elif sys.platform.startswith('linux'):
            binary_path = 'dist/Heroes3MapJournal-linux'
        else:
            self.skipTest("Skipping test: cannot find Operating System")
            return

        # Start the binary
        process = subprocess.Popen([binary_path])

        # Wait a few seconds to ensure the GUI is fully loaded
        time.sleep(5)

        # Close the GUI application using pyautogui if not headless
        if sys.platform == 'win32':
            if not is_headless():
                pyautogui.hotkey('alt', 'f4')  # On Windows
        elif sys.platform == 'darwin':
            if not is_headless():
                pyautogui.hotkey('command', 'q')  # On macOS
        elif sys.platform.startswith('linux'):
            if not is_headless():
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
