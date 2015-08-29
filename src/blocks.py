# -*- coding: utf-8 -*-


class Block:
    blocks = []
    from_id = {}

    def __init__(self, ID, rep='0'):
        self.ID = ID
        self.rep = rep

        Block.blocks.append(self)
        Block.from_id[ID] = self

    def __str__(self):
        return self.rep

    def __repr__(self):
        return self.rep

    def __bool__(self):
        return bool(self.ID)


class Mineral(Block):
    blocks = []
    probs = []

    def __init__(self, ID, strat=range(0, 0), prob=1.0, rep='a'):
        super().__init__(ID, rep)
        self.strat = strat
        self.prob = prob

        Mineral.add_block(self)

    @classmethod
    def add_block(cls, block):
        cls.blocks.append(block)
        cls.probs = []
        for block in cls.blocks:
            cls.probs += [block] * block.prob
        while len(cls.probs) < 1000:
            cls.probs.append(STONE)

# Base blocks
AIR = Block(0, rep='0')
STONE = Block(1, rep='s')
DIRT = Block(2, rep='U')
GRASS = Block(3, rep='h')
COBBLE = Block(4, rep='x')
STEM = Block(5, rep='O')
LEAVES = Block(6, rep='P')

# Minerals
SAPHIR = Mineral(ID=7, strat=range(0, 10), prob=3, rep='r')
EMERALD = Mineral(ID=8, strat=range(0, 10), prob=3, rep='u')
RUBY = Mineral(ID=9, strat=range(0, 10), prob=3, rep='i')
DIAMOND = Mineral(ID=10, strat=range(0, 3), prob=1, rep='y')
GOLD = Mineral(ID=11, strat=range(0, 7), prob=2, rep='a')

#suite
PLANKS = Block(ID=12, rep='m')
WINDOW = Block(ID=13, rep='v')
LIGHT_PLANKS = Block(ID=14, rep='n')
TOIT = Block(ID=15, rep='t')
EAU = Block(ID=16, rep='e')
SNOW = Block(ID=17, rep='I')
INDES = Block(ID=18, rep='p')
COMMERCANT = Block(ID=19, rep='c')
PASSANT = Block(ID=20, rep='1')
PASSANT2 = Block(ID=21, rep='2')
PASSANT3 = Block(ID=22, rep='3')
PASSANT4 = Block(ID=23, rep='4')
PASSANT5 = Block(ID=24, rep='5')
PASSANT6 = Block(ID=25, rep='6')
PASSANT7 = Block(ID=26, rep='7')
PASSANT8 = Block(ID=27, rep='8')