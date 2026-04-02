from .sokoban_state import SokobanState

SOKOBAN_PROBLEMS = (
    # 问题0
    SokobanState("START",
                 0,
                 None,
                 6, 4,  # dimensions
                 ((2, 1), (2, 2)),  # robots
                 frozenset(((1, 1), (1, 2), (4, 1), (4, 2))),  # boxes
                 frozenset(((2, 1), (2, 2), (3, 1), (3, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题1
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((2, 1), (2, 3)),  # robots
                 frozenset(((1, 1), (1, 3), (3, 1), (3, 3))),  # boxes
                 frozenset(((0, 0), (0, 4), (4, 0), (4, 4))),  # storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)))  # obstacles
                 ),
    # 问题2
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((2, 2),),  # robots
                 frozenset(((1, 1), (1, 3), (3, 1), (3, 3))),  # boxes
                 frozenset(((0, 0), (0, 4), (4, 0), (4, 4))),  # storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)))  # obstacles
                 ),
    # 问题3
    SokobanState("START",
                 0,
                 None,
                 6, 4,  # dimensions
                 ((2, 1), (2, 2)),  # robots
                 frozenset(((1, 1), (4, 2))),  # boxes
                 frozenset(((2, 1), (2, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题4
    SokobanState("START",
                 0,
                 None,
                 6, 4,  # dimensions
                 ((2, 1), (2, 2)),  # robots
                 frozenset(((4, 2),)),  # boxes
                 frozenset(((2, 1),)),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题5
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((4, 0), (4, 4)),  # robots
                 frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                 frozenset(((0, 0), (0, 2), (0, 4))),  # storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                 ),
    # 问题6
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((4, 0), (4, 4)),  # robots
                 frozenset(((3, 1), (3, 2))),  # boxes
                 frozenset(((0, 0), (0, 2))),  # storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                 ),
    # 问题7
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((4, 0),),  # robots
                 frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                 frozenset(((0, 0), (0, 2), (0, 4))),  # storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                 ),
    # 问题8
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((0, 0), (0, 2), (0, 4)),  # robots
                 frozenset(((1, 0), (1, 2), (1, 4))),  # boxes
                 frozenset(((5, 0), (5, 2), (0, 5))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题9
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((0, 0), (0, 2), (0, 4), (5, 5)),  # robots
                 frozenset(((1, 0), (4, 1), (1, 2), (4, 3), (1, 4), (4, 5))),  # boxes
                 frozenset(((5, 0), (0, 1), (5, 2), (0, 3), (5, 4), (0, 5))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题10
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((5, 5), (5, 4), (4, 5)),  # robots
                 frozenset(((3, 1), (2, 2), (1, 4), (3, 4))),  # boxes
                 frozenset(((0, 0), (0, 1), (1, 0), (1, 1))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题11
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((5, 5), (5, 4), (4, 5)),  # robots
                 frozenset(((3, 1), (1, 4), (3, 4))),  # boxes
                 frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题12
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((5, 5), (5, 4), (4, 5)),  # robots
                 frozenset(((3, 1), (2, 2), (1, 4))),  # boxes
                 frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题13
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((5, 5), (5, 4)),  # robots
                 frozenset(((3, 1), (1, 4), (3, 4))),  # boxes
                 frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题14
    SokobanState("START",
                 0,
                 None,
                 6, 6,  # dimensions
                 ((5, 5), (5, 4)),  # robots
                 frozenset(((3, 1), (2, 2), (1, 4))),  # boxes
                 frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题15
    SokobanState("START",
                 0,
                 None,
                 8, 8,  # dimensions
                 ((0, 5), (1, 6), (2, 7)),  # robots
                 frozenset(((5, 6), (4, 5), (6, 2), (5, 2), (4, 6))),  # boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题16
    SokobanState("START",
                 0,
                 None,
                 8, 8,  # dimensions
                 ((0, 5), (1, 6), (2, 7)),  # robots
                 frozenset(((6, 2), (5, 6), (4, 4), (6, 3))),  # boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题17
    SokobanState("START",
                 0,
                 None,
                 8, 8,  # dimensions
                 ((0, 5), (1, 6), (2, 7)),  # robots
                 frozenset(((5, 4), (5, 5), (6, 3), (4, 2), (6, 5), (5, 3))),  # boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题18
    SokobanState("START",
                 0,
                 None,
                 8, 8,  # dimensions
                 ((0, 5), (1, 6), (2, 7)),  # robots
                 frozenset(((6, 6), (5, 6), (6, 2), (4, 3), (5, 1), (6, 5))),  # boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题19
    SokobanState("START",
                 0,
                 None,
                 8, 8,  # dimensions
                 ((0, 5), (1, 6), (2, 7)),  # robots
                 frozenset(((6, 6), (4, 5), (4, 1), (4, 3), (5, 2), (5, 3))),  # boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                 frozenset()  # obstacles
                 ),
    # 问题20
    SokobanState("START",
                 0,
                 None,
                 5, 5,  # dimensions
                 ((4, 0),),  # robots
                 frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                 frozenset(((0, 0), (0, 2), (3, 2))),  # storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                 ),
    # 问题21
    SokobanState("START",
                 0,
                 None,
                 4, 7,  # dimensions
                 ((0, 3),),  # robots
                 frozenset(((1, 2), (1, 3), (1, 4))),  # boxes
                 frozenset(((2, 1), (2, 5), (1, 3))),  # storage
                 frozenset(((1, 1), (1, 5)))  # obstacles
                 )
    # 共计 22 测试问题
)
