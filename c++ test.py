import numpy as np

import Ray

array = np.array([
   [
    [ 0, 1, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0],
    [-2, 0,-2, 0],
   ],
  ])

oldarray = np.array([
  [
    [ 0, 0, 0, 0],
    [ 0, 1, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0],
  ],
  [
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0, 0, 0],
    [ 0, 0,-1, 0],
  ],
 ])

array = np.array([
  [
    [ 0, 0, 0, 6],
    [ 0, 2, 0, 2],
    [ 0, 0, 0, 0],
    [-6,-3, 0, 0],
  ],
])

array = np.array([
  [
    [-6, 0, 0, 0, 0, 6],
    [ 0, 0, 0, 0, 2 ,0],
    [ 0, 0, 0, 0, 3 ,0],
    [ 0, 0, 2, 0, 0 ,0],
  ],
])
array = np.array([
  [
    [-6, 0, 0, 0, 0, 6],
    [-4, 0,-1, 0, 0 ,0],
    [ 0, 0, 0, 0, 3 ,0],
    [ 0, 0,-3, 0, 0 ,0],
  ],
])
guy = Ray.Chess_AI(np.ascontiguousarray(array), 1, False)

moves = guy.get_moves()
print(guy.best_move(1))

if not moves:
  if check:
    print('CHECKMATE')
  else:
    print('DRAW')
else:
  print(f'{len(moves)} moves available')
