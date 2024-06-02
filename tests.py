import unittest
import subprocess
import sys
import time
import pyautogui

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """
        CI/CD workflow triggers on pushing this repo to upstream on Github.
        Github actions will build binaries for Windows, MacOS, and Linux and run below command
        
        pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=. Heroes3MapLiker.py
        
        (explanation: create one binary which wont start terminal on binary start e.g. like -mwindows, and embed the icon file
        and place binary in dist folder online so that below tests.py relative filepaths can find them)

        You can test locally by running command above to generate bin in root ./ then run this test to confirm working.
        
        This test then runs to determine if each binary for each OS closes with exit code 0.

        Because program runs in a loop awaiting a Tk window event close, the pyautogui library will simulate
        manually closing app to see results of test.

        As CI/CD pipeline runs jobs to build all OS, it will test to see which binary exists then run that executable test

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        if sys.platform == 'win32':  # Check if running on Windows
            binary_path = 'Heroes3MapLiker.exe'
        elif sys.platform == 'darwin':  # Check if running on macOS
            binary_path = './Heroes3MapLiker'
        elif sys.platform.startswith('linux'):  # Check if running on Linux
            binary_path = './Heroes3MapLiker'

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
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGUI)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
