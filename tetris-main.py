from typing import List

import pygame, random, datetime
from string import Template

BLOCK_SIZE = 30
FIELD_SIZE_X = 10
FIELD_SIZE_Y = 20
GUIDELINES = ["NES like", "Current"]


class Block:
    def __init__(self, color):
        self.color_str = str(color)
        self.color = pygame.Color(color)

    def __str__(self):
        return f"Block {self.color_str}"

    def __repr__(self):
        return f"Block {self.color_str}"


TETROMINOS = [
    [
        [
            [None, None, Block((240, 160, 0)), None],
            [Block((240, 160, 0)), Block((240, 160, 0)), Block((240, 160, 0)), None],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, Block((240, 160, 0)), None, None],
            [None, Block((240, 160, 0)), None, None],
            [None, Block((240, 160, 0)), Block((240, 160, 0)), None],
            [None, None, None, None]
        ],
        [
            [None, None, None, None],
            [Block((240, 160, 0)), Block((240, 160, 0)), Block((240, 160, 0)), None],
            [Block((240, 160, 0)), None, None, None],
            [None, None, None, None]
        ],
        [
            [Block((240, 160, 0)), Block((240, 160, 0)), None, None],
            [None, Block((240, 160, 0)), None, None],
            [None, Block((240, 160, 0)), None, None],
            [None, None, None, None]
        ]

    ],  # 0, L
    [

        [
            [Block((0, 0, 240)), None, None, None],
            [Block((0, 0, 240)), Block((0, 0, 240)), Block((0, 0, 240)), None],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, Block((0, 0, 240)), Block((0, 0, 240)), None],
            [None, Block((0, 0, 240)), None, None],
            [None, Block((0, 0, 240)), None, None],
            [None, None, None, None]
        ],
        [
            [None, None, None, None],
            [Block((0, 0, 240)), Block((0, 0, 240)), Block((0, 0, 240)), None],
            [None, None, Block((0, 0, 240)), None],
            [None, None, None, None]
        ],
        [
            [None, Block((0, 0, 240)), None, None],
            [None, Block((0, 0, 240)), None, None],
            [Block((0, 0, 240)), Block((0, 0, 240)), None, None],
            [None, None, None, None]
        ]
    ],  # 1, J
    [
        [
            [None, Block((0, 240, 0)), Block((0, 240, 0)), None],
            [Block((0, 240, 0)), Block((0, 240, 0)), None, None],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, Block((0, 240, 0)), None, None],
            [None, Block((0, 240, 0)), Block((0, 240, 0)), None],
            [None, None, Block((0, 240, 0)), None],
            [None, None, None, None]
        ],
        [
            [None, None, None, None],
            [None, Block((0, 240, 0)), Block((0, 240, 0)), None],
            [Block((0, 240, 0)), Block((0, 240, 0)), None, None],
            [None, None, None, None]
        ],
        [
            [Block((0, 240, 0)), None, None, None],
            [Block((0, 240, 0)), Block((0, 240, 0)), None, None],
            [None, Block((0, 240, 0)), None, None],
            [None, None, None, None]
        ]
    ],  # 2, S
    [
        [
            [Block((240, 0, 0)), Block((240, 0, 0)), None, None],
            [None, Block((240, 0, 0)), Block((240, 0, 0)), None],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, None, Block((240, 0, 0)), None],
            [None, Block((240, 0, 0)), Block((240, 0, 0)), None],
            [None, Block((240, 0, 0)), None, None],
            [None, None, None, None]
        ],
        [
            [None, None, None, None],
            [Block((240, 0, 0)), Block((240, 0, 0)), None, None],
            [None, Block((240, 0, 0)), Block((240, 0, 0)), None],
            [None, None, None, None]
        ],
        [
            [None, Block((240, 0, 0)), None, None],
            [Block((240, 0, 0)), Block((240, 0, 0)), None, None],
            [Block((240, 0, 0)), None, None, None],
            [None, None, None, None]
        ]
    ],  # 3, Z
    [
        [
            [None, Block((160, 0, 240)), None, None],
            [Block((160, 0, 240)), Block((160, 0, 240)), Block((160, 0, 240)), None],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, Block((160, 0, 240)), None, None],
            [None, Block((160, 0, 240)), Block((160, 0, 240)), None],
            [None, Block((160, 0, 240)), None, None],
            [None, None, None, None]
        ],
        [
            [None, None, None, None],
            [Block((160, 0, 240)), Block((160, 0, 240)), Block((160, 0, 240)), None],
            [None, Block((160, 0, 240)), None, None],
            [None, None, None, None]
        ],
        [
            [None, Block((160, 0, 240)), None, None],
            [Block((160, 0, 240)), Block((160, 0, 240)), None, None],
            [None, Block((160, 0, 240)), None, None],
            [None, None, None, None]
        ]
    ],  # 4, T
    [
        [
            [None, None, None, None],
            [Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240))],
            [None, None, None, None],
            [None, None, None, None]
        ],
        [
            [None, None, Block((0, 240, 240)), None],
            [None, None, Block((0, 240, 240)), None],
            [None, None, Block((0, 240, 240)), None],
            [None, None, Block((0, 240, 240)), None]
        ],
        [
            [None, None, None, None],
            [None, None, None, None],
            [Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240))],
            [None, None, None, None]
        ],
        [
            [None, Block((0, 240, 240)), None, None],
            [None, Block((0, 240, 240)), None, None],
            [None, Block((0, 240, 240)), None, None],
            [None, Block((0, 240, 240)), None, None]
        ]

    ],  # 5, I
    [
        [
            [Block((255, 240, 0)), Block((255, 240, 0)), None, None],
            [Block((255, 240, 0)), Block((255, 240, 0)), None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
    ]   # 6, O
]


class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    hours += d["D"] * 24
    d["S"] = '{:02d}'.format(seconds)
    d["s"] = seconds
    t = DeltaTemplate(fmt)
    d["Z"] = '{:02d}'.format(int(tdelta.microseconds / 10000))
    d["z"] = '{:1d}'.format(int(tdelta.microseconds / 100000))
    d["H"] = hours
    d["M"] = '{:02d}'.format(minutes)
    d["m"] = minutes
    return t.substitute(**d)


def speed_and_lines_for_levels(level):
    if level == 0:
        return 48, 10
    elif level == 1:
        return 43, 20
    elif level == 2:
        return 38, 30
    elif level == 3:
        return 33, 40
    elif level == 4:
        return 28, 50
    elif level == 5:
        return 23, 60
    elif level == 6:
        return 18, 70
    elif level == 7:
        return 13, 80
    elif level == 8:
        return 8, 90
    elif level == 9:
        return 6, 100
    elif 10 <= level <= 12:
        return 5, 100
    elif 13 <= level <= 15:
        return 4, 100
    elif level == 16:
        return 3, 110
    elif level == 17:
        return 3, 120
    elif level == 18:
        return 3, 130
    elif level == 19:
        return 2, 140
    elif level == 20:
        return 2, 150
    elif level == 21:
        return 2, 160
    elif level == 22:
        return 2, 170
    elif level == 23:
        return 2, 180
    elif level == 24:
        return 2, 190
    elif 25 <= level <= 28:
        return 2, 200
    else:
        return 1, 200


class TetrisGameplay:
    def __init__(self, size_x=FIELD_SIZE_X, size_y=FIELD_SIZE_Y, level=0, buffer_zone=20, srs=True, lock_delay=True, seven_bag=True, ghost_piece=True, hold=True, hard_drop=True, handling=(167, 33), nes_mechanics=False, next_len=3):
        self.buffer_y = buffer_zone
        self.FIELD = list(range(size_y + buffer_zone))
        y = 0
        while y != len(self.FIELD):
            self.FIELD[y] = list(range(size_x))
            x = 0
            while x != size_x:
                self.FIELD[y][x] = None
                x += 1
            y += 1
        self.current_posx = 4
        self.current_posy = self.buffer_y - 2
        self.can_hard_drop = hard_drop
        self.support_combo_and_btb_bonuses = False
        self.support_srs = srs
        self.handling = handling
        self.support_hold = hold
        self.nes_mechanics = nes_mechanics
        self.support_ghost_piece = ghost_piece
        self.support_lock_delay = lock_delay
        self.support_garbage = False
        self.seven_bag_random = seven_bag
        self.next_length = next_len
        self.score = [
            0,  # 0, Soft Drop
            0,  # 1, Hard Drop
            0,  # 2, Single
            0,  # 3, Double
            0,  # 4, Triple
            0,  # 5, Tetris
            0,  # 6, T-Spin Mini no lines
            0,  # 7, T-Spin Mini Single
            0,  # 8, T-Spin Mini Double
            0,  # 9, T-Spin no lines
            0,  # 10, T-Spin Single
            0,  # 11, T-Spin Double
            0,  # 12, T-Spin Triple
            0,  # 13, Combo Bonus
            0   # 14, Back-to-Back bonus
        ]
        self.cleared_lines = [
            0,  # Single
            0,  # Double
            0,  # Triple
            0   # Tetris
        ]
        self.pieces = [
            0,  # L piece
            0,  # J piece
            0,  # S piece
            0,  # Z piece
            0,  # T piece
            0,  # I piece
            0   # O piece
        ]
        self.game_time = 0
        self.next_queue = []
        if self.seven_bag_random:
            self.next_queue = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(self.next_queue)
            self.current_id = self.next_queue[0]
            self.next_queue.pop(0)
        else:
            self.current_id = random.randint(0, 6)
            self.next_queue = [random.randint(0, 6) for i in range(self.next_length+1)]
        self.hold_id = None
        self.hold_locked = False
        self.spin_is_last_move = False
        self.spin_is_kick_t_piece = False
        self.current_spin_id = 0
        self.pieces[self.current_id] += 1
        self.lock_delay_run = False
        self.lock_delay_frames = 30
        self.lines_for_level_up = speed_and_lines_for_levels(level)[1]
        self.start_level = level
        self.level = level
        self.game_over = False

    def spawn_tetromino(self):
        if self.collision(4, self.buffer_y-2, self.next_queue[0], 0):
            self.game_over = True
        self.current_posx = 4
        self.current_posy = self.buffer_y - 2
        self.current_id = self.next_queue[0]
        self.hold_locked = False
        self.spin_is_last_move = False
        self.spin_is_kick_t_piece = False
        self.pieces[self.current_id] += 1
        self.current_spin_id = 0
        self.next_queue.pop(0)
        if len(self.next_queue) == self.next_length:
            if self.seven_bag_random:
                next_bag = [0, 1, 2, 3, 4, 5, 6]
                random.shuffle(next_bag)
                self.next_queue.extend(next_bag)
            else:
                ext = [random.randint(0, 6) for i in range(self.next_length+1)]
                self.next_queue.extend(ext)

    def hold_tetromino(self):
        self.current_spin_id = 0
        self.spin_is_kick_t_piece = False
        self.reset_lock_delay()
        if self.hold_id is not None:
            self.current_id, self.hold_id = self.hold_id, self.current_id
            self.current_posx = 4
            self.current_posy = self.buffer_y - 2
            self.hold_locked = True
        else:
            self.hold_id = self.current_id
            self.spawn_tetromino()
            self.hold_locked = True

    def __str__(self):
        return f"size_x={len(self.FIELD[0])}, size_y={len(self.FIELD)}, buffer_y: {self.buffer_y}"

    def clear_lines(self):
        cleared = 0
        frames_delay = 0
        t_spin = False
        t_spin_mini = False
        height = None
        t_spin_corners = [
            [[(0, 0), (2, 0)], [(0, 2), (2, 2)]],
            [[(2, 0), (2, 2)], [(0, 0), (0, 2)]],
            [[(0, 2), (2, 2)], [(0, 0), (2, 0)]],
            [[(0, 2), (0, 0)], [(2, 0), (2, 2)]]
        ]
        if self.current_id == 4 and self.spin_is_last_move:
            front_col = 0
            back_col = 0
            for i in t_spin_corners[self.current_spin_id][0]:
                if self.current_posy+i[1] >= len(self.FIELD) or self.current_posx+i[0] >= len(self.FIELD[self.current_posy+i[1]]) or self.current_posy+i[1] < 0 or self.current_posx+i[0] < 0 or self.FIELD[self.current_posy+i[1]][self.current_posx+i[0]] is not None:
                    front_col += 1
            for i in t_spin_corners[self.current_spin_id][1]:
                if self.current_posy+i[1] >= len(self.FIELD) or self.current_posx+i[0] >= len(self.FIELD[self.current_posy+i[1]]) or self.current_posy+i[1] < 0 or self.current_posx+i[0] < 0 or self.FIELD[self.current_posy+i[1]][self.current_posx+i[0]] is not None:
                    back_col += 1
            if (front_col == 2 and back_col >= 1) or (back_col == 2 and front_col == 1 and self.spin_is_kick_t_piece):
                t_spin = True
            elif back_col == 2 and front_col == 1:
                t_spin_mini = True
        y = len(self.FIELD)
        for i in self.FIELD:
            ic = 0
            for k in i:
                if k is not None:
                    ic += 1
            if ic == FIELD_SIZE_X:
                cleared += 1
                self.FIELD.remove(i)
                new = list(range(FIELD_SIZE_X))
                x = 0
                while x != FIELD_SIZE_X:
                    new[x] = None
                    x += 1
                self.FIELD.insert(0, new)
            y -= 1
            if ic > 0 and height is None:
                height = y

        if cleared > 0:
            self.cleared_lines[cleared - 1] += cleared
            if t_spin:
                if cleared == 1:
                    self.score[10] += 800 * (min(self.level, 29) + 1)
                elif cleared == 2:
                    self.score[11] += 1200 * (min(self.level, 29) + 1)
                elif cleared == 3:
                    self.score[12] += 1600 * (min(self.level, 29) + 1)
            elif t_spin_mini:
                if cleared == 1:
                    self.score[7] += 200 * (min(self.level, 29) + 1)
                elif cleared == 2:
                    self.score[8] += 400 * (min(self.level, 29) + 1)
            if cleared == 1:
                self.score[2] += 100 * (min(self.level, 29) + 1)
            elif cleared == 2:
                self.score[3] += 300 * (min(self.level, 29) + 1)
            elif cleared == 3:
                self.score[4] += 500 * (min(self.level, 29) + 1)
            elif cleared == 4:
                self.score[5] += 800 * (min(self.level, 29) + 1)
            if sum(self.cleared_lines) >= self.lines_for_level_up:
                self.level += 1
                self.lines_for_level_up += 10
        else:
            if t_spin:
                self.score[9] += 400 * (min(self.level, 29) + 1)
            elif t_spin_mini:
                self.score[6] += 100 * (min(self.level, 29) + 1)
        return 0

    def collision(self, next_posx, next_posy, next_id, next_spin_id):
        i1 = next_posy
        k1 = next_posx
        for i in TETROMINOS[next_id][next_spin_id]:
            for k in i:
                if k and (i1 >= len(self.FIELD) or k1 >= len(self.FIELD[i1]) or i1 < 0 or k1 < 0 or self.FIELD[i1][k1]):
                    return True
                k1 += 1
            k1 = next_posx
            i1 += 1
        return False

    def spin(self, reverse=False):
        self.reset_lock_delay()
        if self.current_id != 6:
            if reverse:
                future_spin_id = self.current_spin_id - 1
            else:
                future_spin_id = self.current_spin_id + 1
            future_spin_id %= 4
            if not self.collision(self.current_posx, self.current_posy, self.current_id, future_spin_id):
                self.current_spin_id = future_spin_id
                self.spin_is_last_move = True
                return
            if self.support_srs:
                if self.current_id != 5:
                    if (self.current_spin_id == 0 or self.current_spin_id == 2) and future_spin_id == 1:
                        if not self.collision(self.current_posx-1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-1, self.current_posy-1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.current_posy -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-1, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            self.spin_is_kick_t_piece = True
                            return
                    elif self.current_spin_id == 1 and (future_spin_id == 0 or future_spin_id == 2):
                        if not self.collision(self.current_posx+1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy+1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            self.spin_is_kick_t_piece = True
                            return
                    elif (self.current_spin_id == 0 or self.current_spin_id == 2) and future_spin_id == 3:
                        if not self.collision(self.current_posx+1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy-1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            self.spin_is_kick_t_piece = True
                            return
                    elif self.current_spin_id == 3 and (future_spin_id == 0 or future_spin_id == 2):
                        if not self.collision(self.current_posx-1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy+1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.current_posy += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            self.spin_is_kick_t_piece = True
                            return
                else:
                    if (self.current_spin_id == 0 and future_spin_id == 1) or (self.current_spin_id == 3 and future_spin_id == 2):
                        if not self.collision(self.current_posx-2, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-2, self.current_posy+1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 2
                            self.current_posy += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            return
                    elif (self.current_spin_id == 1 and future_spin_id == 0) or (self.current_spin_id == 2 and future_spin_id == 3):
                        if not self.collision(self.current_posx+2, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+2, self.current_posy-1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 2
                            self.current_posy -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-1, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            return
                    elif (self.current_spin_id == 1 and future_spin_id == 2) or (self.current_spin_id == 0 and future_spin_id == 3):
                        if not self.collision(self.current_posx-1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+2, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-1, self.current_posy-2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 1
                            self.current_posy -= 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+2, self.current_posy+1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 2
                            self.current_posy += 1
                            self.spin_is_last_move = True
                            return
                    elif (self.current_spin_id == 2 and future_spin_id == 1) or (self.current_spin_id == 3 and future_spin_id == 0):
                        if not self.collision(self.current_posx+1, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-2, self.current_posy, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx+1, self.current_posy+2, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx += 1
                            self.current_posy += 2
                            self.spin_is_last_move = True
                            return
                        elif not self.collision(self.current_posx-2, self.current_posy-1, self.current_id, future_spin_id):
                            self.current_spin_id = future_spin_id
                            self.current_posx -= 2
                            self.current_posy -= 1
                            self.spin_is_last_move = True
                            return

    def move_side(self, x_change):
        if not self.collision(self.current_posx + x_change, self.current_posy, self.current_id, self.current_spin_id):
            self.current_posx += x_change
            self.reset_lock_delay()
            self.spin_is_last_move = False

    def save_state(self):
        i1 = self.current_posy
        k1 = self.current_posx
        if self.current_id is not None:
            for i in TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k:
                        self.FIELD[i1][k1] = k
                    k1 += 1
                k1 = self.current_posx
                i1 += 1

    def ghost_piece_y(self):
        y = self.current_posy
        while not self.collision(self.current_posx, y + 1, self.current_id,
                                 self.current_spin_id):
            y += 1
        return y

    def reset_lock_delay(self):
        self.lock_delay_frames = 30
        self.lock_delay_run = False

    def move_down(self, by_player=False, instant=False):
        if not self.collision(self.current_posx, self.current_posy + 1, self.current_id, self.current_spin_id):
            if instant:
                add_to_score = 0
                while not self.collision(self.current_posx, self.current_posy + 1, self.current_id,
                                         self.current_spin_id):
                    self.current_posy += 1
                    add_to_score += 2
                self.score[1] += add_to_score
                self.spin_is_last_move = False
            else:
                self.current_posy += 1
                self.spin_is_last_move = False
                if by_player:
                    self.score[0] += 1
            return True
        else:
            return False

    def draw_game(self):
        win.fill((25, 25, 25))
        pygame.draw.rect(win, (0, 0, 0),
                         (5, (BLOCK_SIZE * 2 + 5), BLOCK_SIZE * FIELD_SIZE_X, BLOCK_SIZE * FIELD_SIZE_Y))
        x = 0
        y = -self.buffer_y
        for i in self.FIELD:
            for k in i:
                window_x = 5 + BLOCK_SIZE * x
                window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * y
                if k is not None:
                    pygame.draw.rect(win, k.color, (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                else:
                    pygame.draw.rect(win, (25, 25, 25), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=1)
                x += 1
            x = 0
            y += 1
        i1 = self.current_posy - self.buffer_y
        k1 = self.current_posx
        if self.current_id is not None:
            for i in TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k is not None:
                        window_x = 5 + BLOCK_SIZE * k1
                        window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                        pygame.draw.rect(win, (int(k.color[0]*self.lock_delay_frames/30), int(k.color[1]*self.lock_delay_frames/30), int(k.color[2]*self.lock_delay_frames/30)), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                    k1 += 1
                k1 = self.current_posx
                i1 += 1
            if self.support_ghost_piece:
                i1 = self.ghost_piece_y() - self.buffer_y
                k1 = self.current_posx
                for i in TETROMINOS[self.current_id][self.current_spin_id]:
                    for k in i:
                        if k is not None:
                            window_x = 5 + BLOCK_SIZE * k1
                            window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                            pygame.draw.rect(win, (k.color[0], k.color[1], k.color[2]), (window_x+5, window_y+5, BLOCK_SIZE-10, BLOCK_SIZE-10), width=10, border_radius=1)
                        k1 += 1
                    k1 = self.current_posx
                    i1 += 1
        x_offset = 0
        for q in range(0, self.next_length):
            i1 = 0
            k1 = 0
            for i in TETROMINOS[self.next_queue[q]][0]:
                for k in i:
                    if k is not None:
                        window_x = 5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + 10 * k1 + x_offset
                        window_y = (BLOCK_SIZE * 2 + 30) + 10 * i1
                        pygame.draw.rect(win, k.color, (window_x, window_y, 10, 10))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 10, 10), width=1)
                    k1 += 1
                k1 = 0
                i1 += 1
            x_offset += 45
        if self.support_hold:
            if self.hold_id is not None:
                i1 = 0
                k1 = 0
                for i in TETROMINOS[self.hold_id][0]:
                    for k in i:
                        if k is not None:
                            window_x = 5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + 10 * k1
                            window_y = (BLOCK_SIZE * 2 + 75) + 10 * i1
                            pygame.draw.rect(win, k.color, (window_x, window_y, 10, 10))
                            pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 10, 10), width=1)
                        k1 += 1
                    k1 = 0
                    i1 += 1
        win.blit(FONT.render("SCORE", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 25 + BLOCK_SIZE * 7))
        total_score = sum(self.score)
        win.blit(FONT.render(f"{total_score:06d}", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 50 + BLOCK_SIZE * 7))
        win.blit(FONT.render("LINES", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 90 + BLOCK_SIZE * 7))
        total_lines = sum(self.cleared_lines)
        win.blit(FONT.render(f"{total_lines:03d}", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 115 + BLOCK_SIZE * 7))
        win.blit(FONT.render("LV", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 155 + BLOCK_SIZE * 7))
        win.blit(FONT.render(f"{self.level:02d}", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 180 + BLOCK_SIZE * 7))
        try:
            tetris_rate = int((self.cleared_lines[3] / total_lines) * 100)
        except ZeroDivisionError:
            tetris_rate = 0
        win.blit(FONT.render("TRT", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 120 + BLOCK_SIZE * k1, 155 + BLOCK_SIZE * 7))
        if tetris_rate == 100:
            win.blit(FONT.render(f"{tetris_rate}", 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 120 + BLOCK_SIZE * k1, 180 + BLOCK_SIZE * 7))
        else:
            win.blit(FONT.render(f"{tetris_rate:02d}%", 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 120 + BLOCK_SIZE * k1, 180 + BLOCK_SIZE * 7))
        win.blit(FONT.render("TIME", 1, (255, 255, 255)),
                 (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 220 + BLOCK_SIZE * 7))
        if self.game_time < 10:
            win.blit(FONT.render(strfdelta(datetime.timedelta(seconds=self.game_time), '%s.%Z'), 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 245 + BLOCK_SIZE * 7))
        elif self.game_time < 60:
            win.blit(FONT.render(strfdelta(datetime.timedelta(seconds=self.game_time), '%S.%z'), 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 245 + BLOCK_SIZE * 7))
        elif self.game_time < 3600:
            win.blit(FONT.render(strfdelta(datetime.timedelta(seconds=self.game_time), '%m:%S'), 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 245 + BLOCK_SIZE * 7))
        else:
            win.blit(FONT.render(strfdelta(datetime.timedelta(seconds=self.game_time), '%H:%M:%S'), 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X + 20 + BLOCK_SIZE * k1, 245 + BLOCK_SIZE * 7))
        if self.game_over:
            text_size_x = FONT.size("GAME")[0]
            pygame.draw.rect(win, (0, 0, 0), (
            BLOCK_SIZE * (FIELD_SIZE_X / 2) - text_size_x, BLOCK_SIZE * FIELD_SIZE_Y / 2, text_size_x * 2 + 10, 60))
            win.blit(FONT.render("GAME", 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X / 2 - text_size_x / 2, 5 + BLOCK_SIZE * FIELD_SIZE_Y / 2))
            win.blit(FONT.render("OVER", 1, (255, 255, 255)),
                     (5 + BLOCK_SIZE * FIELD_SIZE_X / 2 - text_size_x / 2, 5 + BLOCK_SIZE * FIELD_SIZE_Y / 2 + 25))
        pygame.display.update()

    def draw_game_stats(self, on_pause):
        win.fill((25, 25, 25))
        if on_pause:
            win.blit(FONT.render("GAME PAUSED", 1, (255, 255, 255)), (25, 25))
        else:
            win.blit(FONT.render("STATISTIC", 1, (255, 255, 255)), (25, 25))
        total_score = sum(self.score)
        win.blit(FONT.render(f"SCORE {total_score:16d}", 1, (255, 255, 255)), (25, 100))
        total_pieces = sum(self.pieces)
        win.blit(FONT.render(f"PIECES {total_pieces:15d}", 1, (255, 255, 255)), (25, 130))
        total_lines = sum(self.cleared_lines)
        win.blit(FONT.render(f"LINES {total_lines:16d}", 1, (255, 255, 255)), (25, 160))
        try:
            tetris_rate = self.cleared_lines[3] / total_lines
        except ZeroDivisionError:
            tetris_rate = 0
        win.blit(FONT.render(f"TETRIS RATE {tetris_rate:10.2%}", 1, (255, 255, 255)), (25, 190))
        win.blit(FONT.render(f"LEVELS           {self.start_level:02d}-{self.level:02d}", 1, (255, 255, 255)), (25, 220))
        win.blit(
            FONT.render(f"TIME {strfdelta(datetime.timedelta(seconds=self.game_time), '%H:%M:%S.%Z'):>17s}", 1, (255, 255, 255)),
            (25, 250))
        win.blit(SMALL_FONT.render(f"BURNED TIMES LINES      PIECES TABLE", 1, (255, 255, 255)), (25, 290))
        win.blit(
            SMALL_FONT.render(f"SINGLE {self.cleared_lines[0]:5d} {self.cleared_lines[0]:5d}      L {self.pieces[0]:<4d} J {self.pieces[1]:<4d}", 1, (255, 255, 255)),
            (25, 310))
        double_times = int(self.cleared_lines[1] / 2)
        win.blit(SMALL_FONT.render(f"DOUBLE {double_times:5d} {self.cleared_lines[1]:5d}      S {self.pieces[2]:<4d} Z {self.pieces[3]:<4d}", 1, (255, 255, 255)),
                 (25, 325))
        triple_times = int(self.cleared_lines[2] / 3)
        win.blit(SMALL_FONT.render(f"TRIPLE {triple_times:5d} {self.cleared_lines[2]:5d}      T {self.pieces[4]:<4d} O {self.pieces[6]:<4d}", 1, (255, 255, 255)),
                 (25, 340))
        tetris_times = int(self.cleared_lines[3] / 4)
        win.blit(SMALL_FONT.render(f"TETRIS {tetris_times:5d} {self.cleared_lines[3]:5d}      I {self.pieces[5]:<10d}", 1, (255, 255, 255)),
                 (25, 355))
        win.blit(SMALL_FONT.render(f"SCORE TABLE", 1, (255, 255, 255)), (25, 380))
        win.blit(SMALL_FONT.render(f"SOFT DROPS {self.score[0]:14d}", 1, (255, 255, 255)), (25, 400))
        win.blit(SMALL_FONT.render(f"HARD DROPS {self.score[1]:14d}", 1, (255, 255, 255)), (25, 415))
        win.blit(SMALL_FONT.render(f"SINGLE {self.score[2]:18d}", 1, (255, 255, 255)), (25, 430))
        win.blit(SMALL_FONT.render(f"DOUBLE {self.score[3]:18d}", 1, (255, 255, 255)), (25, 445))
        win.blit(SMALL_FONT.render(f"TRIPLE {self.score[4]:18d}", 1, (255, 255, 255)), (25, 460))
        win.blit(SMALL_FONT.render(f"TETRIS {self.score[5]:18d}", 1, (255, 255, 255)), (25, 475))
        win.blit(SMALL_FONT.render(f"T-SPIN MINI NO L. {self.score[6]:7d}", 1, (255, 255, 255)), (25, 490))
        win.blit(SMALL_FONT.render(f"T-SPIN MINI SINGLE {self.score[7]:6d}", 1, (255, 255, 255)), (25, 505))
        win.blit(SMALL_FONT.render(f"T-SPIN MINI DOUBLE {self.score[8]:6d}", 1, (255, 255, 255)), (25, 520))
        win.blit(SMALL_FONT.render(f"T-SPIN NO LINES {self.score[9]:9d}", 1, (255, 255, 255)), (25, 535))
        win.blit(SMALL_FONT.render(f"T-SPIN SINGLE {self.score[10]:11d}", 1, (255, 255, 255)), (25, 550))
        win.blit(SMALL_FONT.render(f"T-SPIN DOUBLE {self.score[11]:11d}", 1, (255, 255, 255)), (25, 565))
        win.blit(SMALL_FONT.render(f"T-SPIN TRIPLE {self.score[12]:11d}", 1, (255, 255, 255)), (25, 580))
        win.blit(SMALL_FONT.render(f"COMBO BONUS {self.score[13]:13d}", 1, (255, 255, 255)), (25, 595))
        win.blit(SMALL_FONT.render(f"BACK-TO-BACK BONUS {self.score[14]:6d}", 1, (255, 255, 255)), (25, 610))
        pygame.display.update()



class NesLikeTetris(TetrisGameplay):
    def __init__(self, size_x=FIELD_SIZE_X, size_y=FIELD_SIZE_Y, level=0):
        super().__init__(size_x, size_y, level, 2, False, False, False, False, False, False, (267, 100), True, 1)

    def __str__(self):
        ans = f"size_x={len(self.FIELD[0])}, size_y={len(self.FIELD)}, Field:"
        for i in self.FIELD:
            ans += f"\n{i}"
        return ans

    def clear_lines(self):
        cleared = 0
        frames_delay = 0
        height = None
        y = len(self.FIELD)
        for i in self.FIELD:
            ic = 0
            for k in i:
                if k is not None:
                    ic += 1
            if ic == FIELD_SIZE_X:
                cleared += 1
                self.FIELD.remove(i)
                new = list(range(FIELD_SIZE_X))
                x = 0
                while x != FIELD_SIZE_X:
                    new[x] = None
                    x += 1
                self.FIELD.insert(0, new)
            y -= 1
            if ic > 0 and height is None:
                height = y
                frames_delay += 10 + (2 * int(height / 4))

        if cleared >= 0:
            self.cleared_lines[cleared - 1] += cleared
            frames_delay += 18
            if cleared == 1:
                self.score[2] += 40 * (min(self.level, 29) + 1)
            elif cleared == 2:
                self.score[3] += 100 * (min(self.level, 29) + 1)
            elif cleared == 3:
                self.score[4] += 300 * (min(self.level, 29) + 1)
            elif cleared == 4:
                self.score[5] += 1200 * (min(self.level, 29) + 1)
            if sum(self.cleared_lines) >= self.lines_for_level_up:
                self.level += 1
                self.lines_for_level_up += 10
        return frames_delay


def draw_main_menu(selected, sel_lvl, sel_gl):
    win.fill((25, 25, 25))
    win.blit(FONT.render("TETRIS by dan63047", 1, (255, 255, 255)), (25, 25))
    win.blit(FONT.render("›", 1, (255, 255, 255)), (25, 100 + 30 * selected))
    win.blit(FONT.render("Start", 1, (255, 255, 255)), (50, 100))
    win.blit(FONT.render(f"Level: {sel_lvl:02d}", 1, (255, 255, 255)), (50, 130))  # ↑↓
    win.blit(FONT.render(f"Guideline: {GUIDELINES[sel_gl]}", 1, (255, 255, 255)), (50, 160))
    pygame.display.update()


def main():
    GAME_RUN = True
    selected_level = 0
    selected_gl = 0
    ticks_before_stats = 180
    ticks_gone = 0
    menu_select = 0
    on_pause = False
    corrupt_hard_drop = False
    field = None
    state = "main menu"
    pygame.key.set_repeat(267, 100)
    while GAME_RUN:
        clock.tick(60)
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_RUN = False
            if event.type == pygame.KEYDOWN:
                pressed_keys.append(event.key)
                if pygame.K_SPACE in pressed_keys and corrupt_hard_drop:
                    pressed_keys.remove(pygame.K_SPACE)
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                corrupt_hard_drop = False
        keys = pygame.key.get_pressed()
        if state == "main menu":
            draw_main_menu(menu_select, selected_level, selected_gl)
            if pygame.K_RETURN in pressed_keys:
                if menu_select == 0:
                    state = "pregameplay"
            if pygame.K_DOWN in pressed_keys and menu_select != 2:
                menu_select += 1
            if pygame.K_UP in pressed_keys and menu_select != 0:
                menu_select -= 1
            if pygame.K_RIGHT in pressed_keys and selected_level != 29 and menu_select == 1:
                selected_level += 1
            elif pygame.K_LEFT in pressed_keys and selected_level != 0 and menu_select == 1:
                selected_level -= 1
            if pygame.K_RIGHT in pressed_keys and selected_gl != 1 and menu_select == 2:
                selected_gl += 1
            elif pygame.K_LEFT in pressed_keys and selected_gl != 0 and menu_select == 2:
                selected_gl -= 1
        elif state == "pregameplay":
            ticks_before_stats = 300
            if selected_gl == 0:
                field = NesLikeTetris(level=selected_level)
            elif selected_gl == 1:
                field = TetrisGameplay(level=selected_level)
            pygame.key.set_repeat(field.handling[0], field.handling[1])
            state = "gameplay"
        elif state == "gameplay":
            field.draw_game()
            ticks_for_down = speed_and_lines_for_levels(field.level)[0]
            if not field.game_over:
                if pygame.K_r in pressed_keys and ticks_gone >= 0:
                    state = "pregameplay"
                if pygame.K_p in pressed_keys and ticks_gone >= 0:
                    on_pause = True
                    state = "gameplay_stats"
                if (pygame.K_UP in pressed_keys or pygame.K_x in pressed_keys) and ticks_gone >= 0:
                    field.spin()
                if pygame.K_z in pressed_keys and ticks_gone >= 0:
                    field.spin(True)
                if pygame.K_c in pressed_keys and ticks_gone >= 0 and field.support_hold and not field.hold_locked:
                    field.hold_tetromino()
                if pygame.K_DOWN in pressed_keys and ticks_gone >= 0:
                    ticks_gone -= field.move_down(True)
                if pygame.K_LEFT in pressed_keys and ticks_gone >= 0:
                    field.move_side(-1)
                if pygame.K_RIGHT in pressed_keys and ticks_gone >= 0:
                    field.move_side(1)
                if pygame.K_SPACE in pressed_keys and not corrupt_hard_drop and field.can_hard_drop:
                    field.move_down(True, True)
                    field.save_state()
                    ticks_gone -= field.clear_lines()
                    field.spawn_tetromino()
                    field.lock_delay_run = False
                    field.lock_delay_frames = 30
                    corrupt_hard_drop = True
                field.game_time += clock.get_time()/1000
            if field.game_over:
                ticks_before_stats -= 1
            ticks_gone += 1
            if ticks_gone >= ticks_for_down:
                ticks_gone = 0
                if not field.game_over:
                    if field.support_lock_delay:
                        if not field.move_down():
                            field.lock_delay_run = True
                    else:
                        if not field.move_down():
                            field.save_state()
                            ticks_gone -= field.clear_lines()
                            field.spawn_tetromino()
            if field.lock_delay_run:
                field.lock_delay_frames -= 1
                if field.lock_delay_frames <= 0 or not field.support_lock_delay:
                    field.save_state()
                    ticks_gone -= field.clear_lines()
                    field.spawn_tetromino()
                    field.reset_lock_delay()
            if ticks_before_stats <= 0:
                state = "gameplay_stats"
        elif state == "gameplay_stats":
            field.draw_game_stats(on_pause)
            if pygame.K_BACKSPACE in pressed_keys:
                state = "main menu"
            elif pygame.K_r in pressed_keys:
                state = "pregameplay"
            if pygame.K_p in pressed_keys:
                on_pause = False
                state = "gameplay"


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((600, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption("dan63047 Tetris")
    pygame.font.init()
    FONT = pygame.font.Font("PressStart2P-vaV7.ttf", 25)
    SMALL_FONT = pygame.font.Font("PressStart2P-vaV7.ttf", 15)
    main()
    pygame.quit()
