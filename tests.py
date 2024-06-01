import unittest
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
from typing import List, Dict
from main import display_gui, load_asset_images

class TestGUI(unittest.TestCase):

    def test_binary_execution(self):
        """
        Github actions CI/CD test on push to upstream repo, CI/CD will build binaries for Windows, MacOS, and Linux
        then run this test file to see if each opens and closes fine with exit code 0

        Returns:
            Return code. 0 = test passed. 1 = test failed.
        """
        windows_binary_path = './Heroes3MapLiker_windows.exe'
        linux_binary_path = './Heroes3MapLiker_linux'
        macos_binary_path = './Heroes3MapLiker_macos'

        # Run binary and capture output
        windows_completed_process = subprocess.run([windows_binary_path], capture_output=True, text=True)
        linux_completed_process = subprocess.run([linux_binary_path], capture_output=True, text=True)
        macos_completed_process = subprocess.run([macos_binary_path], capture_output=True, text=True)

        # Check if the binary executed successfully (exit code 0)
        self.assertEqual(windows_completed_process.returncode, 0)
        self.assertEqual(linux_completed_process.returncode, 0)
        self.assertEqual(macos_completed_process.returncode, 0)

        # # Check if the output contains expected results
        # expected_output = "Expected output string"
        # self.assertIn(expected_output, windows_completed_process.stdout)
        # self.assertIn(expected_output, linux_completed_process.stdout)
        # self.assertIn(expected_output, macos_completed_process.stdout)

    def test_display_gui(self):
        """
        Github actions CI/CD test on push to upstream repo, CI/CD will build binaries for Windows, MacOS, and Linux
        then run this test file

        Returns:
            Pass or fail for test
        """
        SCREEN_WIDTH: int = 1100
        SCREEN_HEIGHT: int = 720
        COLS: int = 1
        IMAGE_WIDTH: int = 300
        IMAGE_HEIGHT: int = 300
        SPACING_X: int = 20
        SPACING_Y: int = 20
        base_dirs: list[str] = ["overworld_map_images", "subterranean_map_images"]
        root = tk.Tk()
        root.title("Heroes 3 Map Liker")
        image_paths: list[str] = [
            "assets/name_descending.png",
            "assets/name_ascending.png",
            "assets/subterranean.png",
            "assets/star.png",
            "assets/page.png",
            "assets/book_open.png",
            "assets/book_closed.png",
            "assets/view_earth.png",
            "assets/dif_easy.gif",
            "assets/dif_expert.gif",
            "assets/dif_hard.gif",
            "assets/dif_impossible.gif",
            "assets/dif_normal.gif",
            "assets/ls_hero.gif",
            "assets/ls_standard.gif",
            "assets/ls_timeexpires.gif",
            "assets/ls_town.gif",
            "assets/m_h3ccmped.png",
            "assets/m_h3maped.png",
            "assets/sz0_s.gif",
            "assets/sz1_m.gif",
            "assets/sz2_l.gif",
            "assets/sz3_xl.gif",
            "assets/sz4_h.gif",
            "assets/sz5_xh.gif",
            "assets/sz6_g.gif",
            "assets/v_ab.gif",
            "assets/v_hota.gif",
            "assets/v_roe.gif",
            "assets/v_sod.gif",
            "assets/v_wog.gif",
            "assets/vc_allmonsters.gif",
            "assets/vc_artifact.gif",
            "assets/vc_buildcity.gif",
            "assets/vc_buildgrail.gif",
            "assets/vc_capturecity.gif",
            "assets/vc_creatures.gif",
            "assets/vc_flagdwellings.gif",
            "assets/vc_flagmines.gif",
            "assets/vc_hero.gif",
            "assets/vc_monster.gif",
            "assets/vc_resources.gif",
            "assets/vc_standard.gif",
            "assets/vc_survivetime.gif",
            "assets/vc_transport.gif",
            "assets/z_backpack.gif",
        ]

        photo_images: Dict[str, ImageTk.PhotoImage] = load_asset_images(image_paths)
        name_descending_photo: ImageTk.PhotoImage = photo_images["name_descending"]
        name_ascending_photo: ImageTk.PhotoImage = photo_images["name_ascending"]
        subterranean_photo: ImageTk.PhotoImage = photo_images["subterranean"]
        liked_photo: ImageTk.PhotoImage = photo_images["star"]
        page_photo: ImageTk.PhotoImage = photo_images["page"]
        book_open_photo: ImageTk.PhotoImage = photo_images["book_open"]
        book_closed_photo: ImageTk.PhotoImage = photo_images["book_closed"]
        view_earth_photo: ImageTk.PhotoImage = photo_images["view_earth"]
        easy_photo: ImageTk.PhotoImage = photo_images["dif_easy"]
        expert_photo: ImageTk.PhotoImage = photo_images["dif_expert"]
        hard_photo: ImageTk.PhotoImage = photo_images["dif_hard"]
        impossible_photo: ImageTk.PhotoImage = photo_images["dif_impossible"]
        normal_photo: ImageTk.PhotoImage = photo_images["dif_normal"]
        ls_hero_photo: ImageTk.PhotoImage = photo_images["ls_hero"]
        ls_standard_photo: ImageTk.PhotoImage = photo_images["ls_standard"]
        ls_timeexpires_photo: ImageTk.PhotoImage = photo_images["ls_timeexpires"]
        ls_town_photo: ImageTk.PhotoImage = photo_images["ls_town"]
        m_h3ccmped_photo: ImageTk.PhotoImage = photo_images["m_h3ccmped"]
        m_h3maped_photo: ImageTk.PhotoImage = photo_images["m_h3maped"]
        sz0_s_photo: ImageTk.PhotoImage = photo_images["sz0_s"]
        sz1_m_photo: ImageTk.PhotoImage = photo_images["sz1_m"]
        sz2_l_photo: ImageTk.PhotoImage = photo_images["sz2_l"]
        sz3_xl_photo: ImageTk.PhotoImage = photo_images["sz3_xl"]
        sz4_h_photo: ImageTk.PhotoImage = photo_images["sz4_h"]
        sz5_xh_photo: ImageTk.PhotoImage = photo_images["sz5_xh"]
        sz6_g_photo: ImageTk.PhotoImage = photo_images["sz6_g"]
        v_ab_photo: ImageTk.PhotoImage = photo_images["v_ab"]
        v_hota_photo: ImageTk.PhotoImage = photo_images["v_hota"]
        v_roe_photo: ImageTk.PhotoImage = photo_images["v_roe"]
        v_sod_photo: ImageTk.PhotoImage = photo_images["v_sod"]
        v_wog_photo: ImageTk.PhotoImage = photo_images["v_wog"]
        vc_allmonsters_photo: ImageTk.PhotoImage = photo_images["vc_allmonsters"]
        vc_artifact_photo: ImageTk.PhotoImage = photo_images["vc_artifact"]
        vc_buildcity_photo: ImageTk.PhotoImage = photo_images["vc_buildcity"]
        vc_buildgrail_photo: ImageTk.PhotoImage = photo_images["vc_buildgrail"]
        vc_capturecity_photo: ImageTk.PhotoImage = photo_images["vc_capturecity"]
        vc_creatures_photo: ImageTk.PhotoImage = photo_images["vc_creatures"]
        vc_flagdwellings_photo: ImageTk.PhotoImage = photo_images["vc_flagdwellings"]
        vc_flagmines_photo: ImageTk.PhotoImage = photo_images["vc_flagmines"]
        vc_hero_photo: ImageTk.PhotoImage = photo_images["vc_hero"]
        vc_monster_photo: ImageTk.PhotoImage = photo_images["vc_monster"]
        vc_resources_photo: ImageTk.PhotoImage = photo_images["vc_resources"]
        vc_standard_photo: ImageTk.PhotoImage = photo_images["vc_standard"]
        vc_survivetime_photo: ImageTk.PhotoImage = photo_images["vc_survivetime"]
        vc_transport_photo: ImageTk.PhotoImage = photo_images["vc_transport"]
        z_backpack_photo: ImageTk.PhotoImage = photo_images["z_backpack"]
                
        # Call the function under test
        display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs)

        # Add assertions to verify the expected behavior or state
        # For example, check if certain widgets are present
        self.assertIsInstance(root, tk.Tk)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
