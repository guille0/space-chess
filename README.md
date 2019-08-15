# space-chess

![Raumschach vr chess](https://raw.githubusercontent.com/guille0/space-chess/master/raumschach.png)

Based on the [Raumschach](https://www.chessvariants.com/3d.dir/3d5.html) chess variant.

**Raumschach** (german for "space chess") is a 3D variant of chess utilizing a 5x5x5 board and including new moves for the pieces to explore the third dimension and a new piece, the unicorn. This is an augmented reality implementation of the game which can be played printing the marker in the /data folder and with a mouse and camera.

The engine also includes an easy way to create any kind of board (config.py). [**Video of a 5x5x3 variant**](https://gfycat.com/passionatelonearmyant).

Includes an AI based on a minimax algorithm with alpha-beta pruning. Since it's written on Python it's really slow for something like Raumshach, but it works alright for smaller boards/puzzles.

Requirements:
```python
pip install panda3d opencv-python numpy
```

Models used: [Chess pieces](https://www.turbosquid.com/FullPreview/Index.cfm/ID/686549)
and [unicorn model](https://free3d.com/3d-model/-chess-knight-v2--942593.html).
