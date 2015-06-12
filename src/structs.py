# -*- coding: utf-8 -*-

from blocks import *
import conditions as condition
import random


class Structure:
    structures = []

    def __init__(self, pattern, base, cond=lambda: True):
        self.pattern = pattern
        self.base = base
        self.cond = cond

        Structure.structures.append(self)

    def substitute(self, x, y):
        base_x, base_y = self.base
        get_absolute = lambda rel_x, rel_y: (x+rel_x, y+rel_y)
        get_relative_from_base = lambda abs_x, abs_y: (abs_x-base_x, abs_y-base_y)

        block_dict = {}
        for iy, line in enumerate(self.pattern()):
            for ix, block in enumerate(line):
                if block is not None:
                    block = Block.from_id[block]
                    abs_pos = get_absolute(*get_relative_from_base(ix, iy))
                    block_dict[abs_pos] = block
        return block_dict.items()

    def __repr__(self):
        return self.pattern()


TREE = Structure(
    lambda: [
        [None, None, None, 6   , 6   , 6   , 6   , None, None, None],
        [None, 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   ],
        [6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   ],
        [6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   ],
        [6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   , 6   ],
        [None, None, 6   , 6   , 6   , 6   , 6   , 6   , None, None],
        [None, None, None, None, 5   , 5   , 5   , None, None, None],
        [None, None, None, None, 5   , 5   , None, None, None, None],
        [None, None, None, None, 5   , 5   , None, None, None, None],
        [None, None, None, None, 5   , 5   , None, None, None, None],
        [None, None, None, None, 5   , 5   , None, None, None, None]
    ],
    base=(4, 10),
    cond=condition.TREE
)

HOUSE = Structure(
   lambda: [
       [None, None, None, 15  , None, None, None],
       [None, None, 15  , 15  , 15  , None, None],
       [None, 15  , 15  , 15  , 15  , 15  , None],
       [15  , 15  , 12  , 12  , 12  , 15  , 15  ],
       [12  , 12  , 12  , 13  , 12  , 12  , 12  ],
       [12  , 13  , 12  , 13  , 12  , 13  , 12  ],
       [12  , 13  , 12  , 13  , 12  , 13  , 12  ],
       [12  , 12  , 12  , 12  , 12  , 12  , 12  ],
       [12  , 12  , 12  , 0   , 12  , 12  , 12  ],
       [12  , 13  , 0   , 0   , 0   , 13  , 12  ],
       [12  , 12  , 0   , random.randint(20, 27), 0   , 12  , 12  ]
   ],
   base=(3, 10),
   cond=condition.HOUSE
)

SHOP = Structure(
    lambda: [
        [None, None, None, 15  , None, None, None],
        [None, None, 15  , 15  , 15  , None, None],
        [None, 15  , 15  , 15  , 15  , 15  , None],
        [15  , 15  , 14  , 14  , 14  , 15  , 15  ],
        [14  , 14  , 14  , 13  , 14  , 14  , 14  ],
        [14  , 13  , 14  , 13  , 14  , 13  , 14  ],
        [14  , 13  , 14  , 13  , 14  , 13  , 14  ],
        [14  , 14  , 14  , 14  , 14  , 14  , 14  ],
        [14  , 14  , 14  , 0   , 14  , 14  , 14  ],
        [14  , 13  , 0   , 0   , 0   , 13  , 14  ],
        [14  , 14  , 0   , 19  , 0   , 14  , 14  ]
    ],
    base=(3, 10),
    cond=condition.HOUSE
)

PONT = Structure(
    lambda: [
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  , 14  ],
        [14  , None, 14  , None, 14  , None, None, None, None, 14  , None, 14  , None, 14  ],
        [None, 14  , 14  , 14  , None, None, None, None, None, None, 14  , 14  , 14  , None],
        [None, None, 14  , 14  , None, None, None, None, None, None, None, 14  , None, None],
        [None, None, 14  , None, None, None, None, None, None, None, None, 14  , None, None],
        [16  , 16  , 14  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , 14  , 16  , 16  ],
        [16  , 16  , 14  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , 14  , 16  , 16  ]
    ],
    base=(1, 10),
    cond=condition.PONT
)

LAKE = Structure(
    lambda: [
        [None, None, 0   , None, None, None, None, 0   , 0   , random.choice([None, 0])],
        [0   , 0   , 0   , 0   , random.choice([None, 0]), random.choice([None, 0]), 0   , 0   , 0   , 0   ],
        [0   , 0   , 0   , 0   , 0   , 0   , 0   , 0   , 0   , 0   ],
        [random.choice([None, 16]), 16  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , random.choice([None, 16])],
        [None, 16  , 16  , 16  , 16  , 16  , 16  , 16  , 16  , None],
        [None, None, random.choice([None, 16]), 16  , 16  , 16  , 16  , 16  , random.choice([None, 16]), None],
    ],
    base=(0, 0),
    cond=condition.LAKE
)