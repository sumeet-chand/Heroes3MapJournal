
# Description

v0.1 - Release date: TBA - I have developed carpal tunnel and typing hurts. I may pay someone one to finish one day. be patient please.

A Heroes of Magic and Might franchise Map Journal and standalone Mod to
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
13. Break up code getting too big, and test with test.py
14. Find HD icons if possible, and make a function to scrap if from a safe repo
15. Convert CI/CD pipeline to have new job of creating binary releases


# Setup

1. No Installation required. Start the software/program/application: ```Heroes3MapLiker```
2. Click ```rescan images``` the first time and wait for all the map images to download then wait for images to download and done.


# Building

There are 2 options to build

1. Manual (locally): by running command with python installed: ```pyinstaller --onefile --noconsole --icon=assets/view_earth.ico --distpath=. Heroes3MapLiker.py``` then test with ```tests.py```
2. Automatic (CI/CD): If making changes to this codebase and pushing  a Github CI/CD pipeline ```.github\workflows\actions.yml``` pushes changes, builds binaries, tests using ./tests.py, if all tests pass, creates releases for each OS


# License

All media, and trademark is copyrighted to the Heroes 3 owners. I strongly encourage you to purchase
the retail version from the developers themselves.
This software and code is provided for non-commercial use and may be modified at the user's discretion.


# Credits

* https://heroes.thelazy.net for providing map info
* Star icon by paomedia (Arnaud) from icon-icons.com
* name_ascending/descending.png by Dave Gandy from icon-icons.com
