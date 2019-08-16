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

# array = np.array([
#    [
#     [ 2, 3, 6, 3, 2],
#     [ 1, 1, 1, 1, 1],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#    ],
#    [
#     [ 4, 7, 5, 7, 4],
#     [ 1, 1, 1, 1, 1],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#    ],
#    [
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#    ],
#    [
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [-1,-1,-1,-1,-1],
#     [-4,-7,-5,-7,-4],
#    ],
#    [
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0],
#     [-1,-1,-1,-1,-1],
#     [-2,-3,-6,-3,-2],
#    ],
#   ])

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
