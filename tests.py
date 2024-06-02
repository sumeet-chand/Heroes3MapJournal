import unittest
import subprocess

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """
        CI/CD workflow triggers on pushing this repo to upstream on Github.
        Github actions will build binaries for Windows, MacOS, and Linux
        using command: pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=dist Heroes3MapLiker.py
        (explanation: create one binary which wont start terminal on binary start e.g. like -mwindows, and embed the icon file
        and place binary in dist folder online so that below tests.py relative filepaths can find them.
        This test then runs to determine if each binary for each OS closes with exit code 0

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        # Adjusted file paths for GitHub Actions workflow
        windows_binary_path = 'dist/Heroes3MapLiker.exe'
        macos_binary_path = 'dist/Heroes3MapLiker'
        linux_binary_path = 'dist/Heroes3MapLiker'

        # Run binary and capture output
        windows_completed_process = subprocess.run([windows_binary_path], capture_output=True, text=True)
        macos_completed_process = subprocess.run([macos_binary_path], capture_output=True, text=True)
        linux_completed_process = subprocess.run([linux_binary_path], capture_output=True, text=True)
        
        # Check if the binary executed successfully (exit code 0)
        self.assertEqual(windows_completed_process.returncode, 0)
        self.assertEqual(macos_completed_process.returncode, 0)
        self.assertEqual(linux_completed_process.returncode, 0)

        # # Check if the output contains expected results
        # expected_output = "Expected output string"
        # self.assertIn(expected_output, windows_completed_process.stdout)
        # self.assertIn(expected_output, linux_completed_process.stdout)
        # self.assertIn(expected_output, macos_completed_process.stdout)

if __name__ == '__main__':
    unittest.main()
