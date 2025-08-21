
# Description

Author: Sumeet Singh
Dated: 20th Aprl 2025
Version: 0.1 - Release date: TBA
License: This project is intended for personal, non-commercial use only. All asset images remain the property of the original owners of Heroes of Might and Magic 3. No endorsement of piracy or commercial use is intended. This software is provided as a hobby project for fans of the game.

Heros3MapJournal is a Heroes of Might and Magic 3 software to download map images, rate them and share notes with others
* Like/Filter/Record/Make notes/Share/Export on won, unfinished and unplayed maps
* Search maps by images with various scenario filters (as well as name) and search within map images
* Launch your Heroes of Might and Magic game launcher directly to the map picked for a new way to play
If you see a missing feature please suggest by contacting author Sumeet Singh @ sumeet-singh.com/contactus


# Roadmap

0. Fix set background image
2. Scrap metadada from URL and save it in JSON format
3. Like image button adds star icon in top right
4. Setup filters
5. Allow taking journal notes for maps
6. Maybe include a feature for sorting between campaign maps
7. Export liked maps button
8. Button to reset liked images, with confirmation popup
9. Allow marking map won (with sword icon in bottom left) and filter by them, and remaining unwon
10. Add option to link to Heroes 3 launcher/original client to bring up in game scenario selection
11. Android/iOS app
12. Expand to Heroes 1, 2 and 4
13. Fix test.py
14. Find HD icons if possible, and make a function to scrap if from a safe repo
15. Convert CI/CD pipeline to have new job of creating binary releases


# Setup

1. No Installation required. Either have Python installed (you can download from here https://www.python.org/downloads/) and run main.py or build yourself for an executable if the relevant release is not bundled.
2. Once you've started the app for the first time click ```rescan images``` and wait for all the map images to download then wait for images to download and done.


# Building

There are 2 options to build

1. Manual (locally): by running command with python installed: ```pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=. main.py``` then test with ```tests.py```
2. Automatic (CI/CD): If making changes to this codebase and pushing  a Github CI/CD pipeline ```.github\workflows\actions.yml``` pushes changes, builds binaries, tests using ./tests.py, if all tests pass, creates releases for each OS


# License

All media, and trademark is copyrighted to the Heroes 3 owners. I strongly encourage you to purchase
the retail version from the developers themselves.
This software and code is provided for non-commercial use and may be modified at the user's discretion.


# Credits

* https://heroes.thelazy.net for providing map info
* Star icon by paomedia (Arnaud) from icon-icons.com
* name_ascending/descending.png by Dave Gandy from icon-icons.com