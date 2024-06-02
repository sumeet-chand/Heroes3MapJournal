import unittest
import subprocess

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """
        Github actions CI/CD test on push to upstream repo, CI/CD will build binaries for Windows, MacOS, and Linux
        then run this test file to see if each opens and closes fine with exit code 0

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        windows_binary_path = './Heroes3MapLiker.exe'
        macos_binary_path = './Heroes3MapLiker'
        linux_binary_path = './Heroes3MapLiker_linux'
        
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
