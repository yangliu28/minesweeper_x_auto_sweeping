# minesweeper_x_auto_sweeping
Python program plays Minesweeper X in Windows. Not cheating like reading the application's memory, but grab the image, do the reasoning, and control the mouse action to solve the game.

## test run
Install python and the dependencies, including [mss](https://python-mss.readthedocs.io/en/dev/index.html), Pillow and win32api.

Open the Minesweeper X application, make sure the game window is not covered by other appications. Then navigate to this program folder in command line and run

`python autominesweeper.py`

## benchmark
The finishing time is pretty steady, 2 seconds for beginner, 5 seconds for intermediate, and 10 seconds for expert. The program hesitates a little when a large empty area is discovered, image capturing is the most time consuming part. Since it is a study for computerized minesweeping strategies, there is no extra intention to improve on that.

![](image\ templates/benchmark.png?raw=true)

