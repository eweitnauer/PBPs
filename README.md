# Physical Bongard Problems #

Physical Bongard Problems (PBPs) are collections of simple 2D physical scenes. Half of the scenes are on the left side, half of them on the right side. Solving the problem means finding the distinguishing difference between both sides. For example, the scenes on the left could all contain an object that will fall to the left, while the scenes on the right all contain an object that will fall to the right.

All PBPs were created by Erik Weitnauer and are his dissertation topic. They are inspired by the classical [Bongard problems](en.wikipedia.org/wiki/Bongard_problem).

Copyright by Erik Weitnauer, 2013.

## Image Files ##

There is one SVG file for each scene. The file name pattern is `{row}-{col}.png`.

Each PBP has at least 20 scenes in this order:

    [1,1] [1,2]  |||  [1,3] [1,4]
    [2,1] [2,2]  |||  [2,3] [2,4]
    [3,1] [3,2]  |||  [3,3] [3,4]
    [4,1] [4,2]  |||  [4,3] [4,4]
    [5,1] [5,2]  |||  [5,3] [5,4]

Each row contains scenes similar to each other. Scenes from different rows are dissimilar to each other.

Some of the scenes might be used for training, others for testing.