import time
from typing import List
import pygame, random, datetime, threading
from string import Template

BLOCK_SIZE = 30
GUIDELINES = ["Modern", "Classic"]
MODES = ["Endless", "Time limited", "Lines limited", "vs Bot (Garbage)", "vs Bot (Score)"]
TIME_LIMITS_SEC = [120, 180, 300, 600, 1800, 3600, 86400]
LINES_LIMITS = [40, 80, 120, 150, 300, 500, 1000]
state = "main menu"
menu_select = 0
selected_gl = 0
selected_mode = 0 # 0 - Endless; 1 - Time limit; 2 - Lines limit
selected_target = 0
session = []

class Block:
    def __init__(self, color):
        self.color_str = str(color)
        self.color = pygame.Color(color)

    def __str__(self):
        return f"Block {self.color_str}"

    def __repr__(self):
        return f"Block {self.color_str}"

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
    d["m"] = minutes + hours*60
    return t.substitute(**d)


class TetrisGameplay:
    def __init__(self, mode=0, lvl=1, buffer_zone=20, player="P1", srs=True, lock_delay=True, seven_bag=True, ghost_piece=True, hold=True, hard_drop=True, handling=(167, 33), nes_mechanics=False, next_len=4, seed=random.randint(-2147483648, 2147483647)):
        self.buffer_y = buffer_zone
        self.FIELD = list(range(20 + buffer_zone))
        y = 0
        self.seed = seed
        self.randomiser = random.Random(seed)
        while y != len(self.FIELD):
            self.FIELD[y] = list(range(10))
            x = 0
            while x != len(self.FIELD[y]):
                self.FIELD[y][x] = None
                x += 1
            y += 1
        self.TETROMINOS = [
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
        self.g = 0
        self.current_posx = 4
        self.player = player
        self.current_posy = self.buffer_y - 2
        self.can_hard_drop = hard_drop
        self.mode = mode
        self.support_combo_and_btb_bonuses = False
        self.support_srs = srs
        self.handling = handling
        self.support_hold = hold
        self.soft_drop = False
        self.soft_drop_speed = 0.5
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
        self.score_up = 0
        self.for_what_id = 0
        self.for_what_score = ["SINGLE", "DOUBLE", "TRIPLE", "QUAD", "T-SPIN MINI", "T-SPIN MINI SINGLE", "T-SPIN MINI DOUBLE", "T-SPIN", "T-SPIN SINGLE", "T-SPIN DOUBLE", "T-SPIN TRIPLE"]
        self.notification = {"for_what": None, "mode": None, "number": None, "combo": None, "b2b": None, "t-spin": False, "t-spin_mini": False, "pc": False, "game_time": None}
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
        self.combo = -1
        self.back_to_back = -1
        self.next_queue = []
        self.garbage_queue = []
        self.attack = 0
        self.send_attack = 0
        if self.seven_bag_random:
            self.next_queue = [0, 1, 2, 3, 4, 5, 6]
            self.randomiser.shuffle(self.next_queue)
            self.current_id = self.next_queue[0]
            self.next_queue.pop(0)
        else:
            self.current_id = self.randomiser.randint(0, 6)
            self.next_queue = [self.randomiser.randint(0, 6) for i in range(self.next_length+1)]
        self.hold_id = None
        self.hold_locked = False
        self.spin_is_last_move = False
        self.spin_is_kick_t_piece = False
        self.current_spin_id = 0
        self.lock_delay_run = False
        if self.mode == 0:
            self.level = lvl
            self.start_level = lvl
        else:
            self.level = 1
            self.start_level = 1
        self.level_limit = 30
        self.lock_delay_f_limit = min(30, 90 - 3 * self.level)
        self.lock_delay_frames = self.lock_delay_f_limit
        self.lock_delay_times_left = 15
        if self.mode == 1:
            self.target = TIME_LIMITS_SEC[lvl]
        elif self.mode == 2:
            self.target = LINES_LIMITS[lvl]
        elif self.mode == 3:
            self.target = 1
            self.support_garbage = True
        self.lines_for_level_up = self.gravity_and_lines_table()[1]
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
        self.lock_delay_times_left = 15
        self.current_spin_id = 0
        self.next_queue.pop(0)
        if len(self.next_queue) == self.next_length:
            if self.seven_bag_random:
                next_bag = [0, 1, 2, 3, 4, 5, 6]
                self.randomiser.shuffle(next_bag)
                self.next_queue.extend(next_bag)
            else:
                ext = [self.randomiser.randint(0, 6) for i in range(self.next_length+1)]
                self.next_queue.extend(ext)

    def hold_tetromino(self):
        self.current_spin_id = 0
        self.spin_is_kick_t_piece = False
        self.reset_lock_delay()
        if self.hold_id is not None:
            self.current_id, self.hold_id = self.hold_id, self.current_id
            self.current_posx = 4
            self.current_posy = self.buffer_y - 2
        else:
            self.hold_id = self.current_id
            self.spawn_tetromino()

        self.hold_locked = True

    def __str__(self):
        return f"size_x={len(self.FIELD[0])}, size_y={len(self.FIELD)}, buffer_y: {self.buffer_y}"

    def gravity_and_lines_table(self):
        return 1 / (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1) * 0.016666, self.level * 10

    def clear_lines(self):
        cleared = 0
        self.send_attack = 0
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
            front_col = sum(
                self.current_posy + i[1] >= len(self.FIELD)
                or self.current_posx + i[0]
                >= len(self.FIELD[self.current_posy + i[1]])
                or self.current_posy + i[1] < 0
                or self.current_posx + i[0] < 0
                or self.FIELD[self.current_posy + i[1]][self.current_posx + i[0]]
                is not None
                for i in t_spin_corners[self.current_spin_id][0]
            )

            back_col = sum(
                self.current_posy + i[1] >= len(self.FIELD)
                or self.current_posx + i[0]
                >= len(self.FIELD[self.current_posy + i[1]])
                or self.current_posy + i[1] < 0
                or self.current_posx + i[0] < 0
                or self.FIELD[self.current_posy + i[1]][self.current_posx + i[0]]
                is not None
                for i in t_spin_corners[self.current_spin_id][1]
            )

            if (front_col == 2 and back_col >= 1) or (back_col == 2 and front_col == 1 and self.spin_is_kick_t_piece):
                t_spin = True
            elif back_col == 2 and front_col == 1:
                t_spin_mini = True
        y = len(self.FIELD)
        for_all_clear = y
        for i in self.FIELD:
            ic = sum(k is not None for k in i)
            if ic == 10:
                cleared += 1
                self.FIELD.remove(i)
                new = list(range(10))
                x = 0
                while x != 10:
                    new[x] = None
                    x += 1
                self.FIELD.insert(0, new)
                for_all_clear -= 1
            elif ic == 0:
                for_all_clear -= 1
            y -= 1
            if ic > 0 and height is None:
                height = y
        all_clear = for_all_clear == 0
        if cleared > 0:
            difficult = False
            self.count_clear(cleared, t_spin, difficult, t_spin_mini, all_clear)
        else:
            self.combo = -1
            if t_spin:
                self.count_no_clear_spin(9, 400, 7, t_spin, t_spin_mini)
            elif t_spin_mini:
                self.count_no_clear_spin(6, 100, 4, t_spin, t_spin_mini)
        self.attack += self.send_attack
        return (0, self.send_attack) if self.support_garbage else 0

    def count_clear(self, cleared, t_spin, difficult, t_spin_mini, all_clear):
        self.cleared_lines[cleared - 1] += cleared
        wt = 0
        if self.mode == 2:
            self.target -= cleared
            if self.target <= 0:
                self.target = 0
                self.game_over = True
        self.combo += 1
        self.score_up = 0
        if t_spin:
            difficult = True
            if cleared == 1:
                self.send_attack = 2
                self.score[10] += 800 * min(self.level, self.level_limit)
                self.score_up += 800 * min(self.level, self.level_limit)
                wt = 8
            elif cleared == 2:
                self.send_attack = 4
                self.score[11] += 1200 * min(self.level, self.level_limit)
                self.score_up += 1200 * min(self.level, self.level_limit)
                wt = 9
            elif cleared == 3:
                self.send_attack = 6
                self.score[12] += 1600 * min(self.level, self.level_limit)
                self.score_up += 1600 * min(self.level, self.level_limit)
                wt = 10
        elif t_spin_mini:
            difficult = True
            if cleared == 1:
                self.send_attack = 0
                self.score[7] += 200 * min(self.level, self.level_limit)
                self.score_up += 200 * min(self.level, self.level_limit)
                wt = 5
            elif cleared == 2:
                self.send_attack = 1
                self.score[8] += 400 * min(self.level, self.level_limit)
                self.score_up += 400 * min(self.level, self.level_limit)
                wt = 6
        elif cleared == 1:
            if all_clear:
                self.send_attack = 10
                self.score[2] += 800 * min(self.level, self.level_limit)
                self.score_up += 800 * min(self.level, self.level_limit)
            else:
                self.send_attack = 0
                self.score[2] += 100 * min(self.level, self.level_limit)
                self.score_up += 100 * min(self.level, self.level_limit)
            wt = 0
        elif cleared == 2:
            if all_clear:
                self.send_attack = 11
                self.score[3] += 1200 * min(self.level, self.level_limit)
                self.score_up += 1200 * min(self.level, self.level_limit)
            else:
                self.send_attack = 1
                self.score[3] += 300 * min(self.level, self.level_limit)
                self.score_up += 300 * min(self.level, self.level_limit)
            wt = 1
        elif cleared == 3:
            if all_clear:
                self.send_attack = 12
                self.score[4] += 1800 * min(self.level, self.level_limit)
                self.score_up += 1800 * min(self.level, self.level_limit)
            else:
                self.send_attack = 2
                self.score[4] += 500 * min(self.level, self.level_limit)
                self.score_up += 500 * min(self.level, self.level_limit)
            wt = 2
        elif cleared == 4:
            if all_clear:
                self.send_attack = 14
                self.score[5] += 2000 * min(self.level, self.level_limit)
                self.score_up += 2000 * min(self.level, self.level_limit)
            else:
                self.send_attack = 4
                self.score[5] += 800 * min(self.level, self.level_limit)
                self.score_up += 800 * min(self.level, self.level_limit)
            wt = 3
            difficult = True
        if sum(self.cleared_lines) >= self.lines_for_level_up and self.level != self.level_limit and self.mode == 0:
            self.level += 1
            self.lines_for_level_up += 10
            self.lock_delay_f_limit = min(30, 90 - 3 * self.level)
        if difficult:
            self.back_to_back += 1
            if self.back_to_back > 0:
                if all_clear:
                    self.score[14] += 1200*min(self.level, self.level_limit)
                    self.score_up += 1200*min(self.level, self.level_limit)
                else:
                    self.score[14] += int((self.score_up*3/2) - self.score_up)
                    self.score_up += int((self.score_up*3/2) - self.score_up)
                self.send_attack += 1
        else:
            self.back_to_back = -1
        if self.combo > 0:
            self.send_attack += int(self.combo / 3) + 1
            self.score[13] += 50 * self.combo * min(self.level, self.level_limit)
            self.score_up += 50 * self.combo * min(self.level, self.level_limit)
        self.notification = {"for_what": wt, "mode": "score", "number": self.score_up, "combo": self.combo,
                             "b2b": self.back_to_back, "t-spin": t_spin, "t-spin_mini": t_spin_mini,
                             "pc": all_clear, "game_time": self.game_time}
        self.for_what_delay = 3

    def count_no_clear_spin(self, wt_id, scr, what, t_spin, t_spin_mini):
        self.score[wt_id] += scr * min(self.level, self.level_limit)
        self.score_up = scr * min(self.level, self.level_limit)
        self.notification = {"for_what": what, "mode": "score", "number": scr, "combo": self.combo, "b2b": self.back_to_back, "t-spin": t_spin, "t-spin_mini": t_spin_mini, "pc": False, "game_time": self.game_time}

    def collision(self, next_posx, next_posy, figure_id, spin_id):
        i1 = next_posy
        k1 = next_posx
        for i in self.TETROMINOS[figure_id][spin_id]:
            for k in i:
                if k and (i1 >= len(self.FIELD) or k1 >= len(self.FIELD[i1]) or i1 < 0 or k1 < 0 or self.FIELD[i1][k1]):
                    return True
                k1 += 1
            k1 = next_posx
            i1 += 1
        return False

    def spin(self, reverse=False):
        if self.current_id is None or self.current_id == 6:
            return
        if reverse:
            future_spin_id = self.current_spin_id - 1
        else:
            future_spin_id = self.current_spin_id + 1
        future_spin_id %= len(self.TETROMINOS[self.current_id])
        KICK_TABLE =   [[(-1, 0),(-1, 1),( 0,-2),(-1,-2)],
                        [( 1, 0),( 1,-1),( 0, 2),( 1, 2)],
                        [( 1, 0),( 1, 1),( 0,-2),( 1,-2)], 
                        [(-1, 0),(-1,-1),( 0, 2),(-1, 2)]]
        KICK_TABLE_I = [[(-2, 0),( 1, 0),(-2,-1),( 1, 2)],
                        [(-1, 0),( 2, 0),(-1, 2),( 2,-1)],
                        [( 2, 0),(-1, 0),( 2, 1),(-1,-2)],
                        [( 1, 0),(-2, 0),( 1,-2),(-2, 1)]]
        if not self.collision(self.current_posx, self.current_posy, self.current_id, future_spin_id):
            self.current_spin_id = future_spin_id
            self.spin_is_last_move = True
        elif self.support_srs:
            if self.current_id is not None and self.current_id != 5:
                if reverse:
                    for kick in KICK_TABLE[future_spin_id]:
                        if not self.collision(self.current_posx-kick[0], self.current_posy+kick[1], self.current_id, future_spin_id):
                            self.current_posx -= kick[0]
                            self.current_posy += kick[1]
                            self.current_spin_id = future_spin_id
                            self.spin_is_last_move = True
                            break
                else:
                    for kick in KICK_TABLE[self.current_spin_id]:
                        if not self.collision(self.current_posx+kick[0], self.current_posy-kick[1], self.current_id, future_spin_id):
                            self.current_posx += kick[0]
                            self.current_posy -= kick[1]
                            self.current_spin_id = future_spin_id
                            self.spin_is_last_move = True
                            break
            elif reverse:
                for kick in KICK_TABLE_I[future_spin_id]:
                    if not self.collision(self.current_posx-kick[0], self.current_posy+kick[1], self.current_id, future_spin_id):
                        self.current_posx -= kick[0]
                        self.current_posy += kick[1]
                        self.current_spin_id = future_spin_id
                        self.spin_is_last_move = True
                        break
            else:
                for kick in KICK_TABLE_I[self.current_spin_id]:
                    if not self.collision(self.current_posx+kick[0], self.current_posy-kick[1], self.current_id, future_spin_id):
                        self.current_posx += kick[0]
                        self.current_posy -= kick[1]
                        self.current_spin_id = future_spin_id
                        self.spin_is_last_move = True
                        break
        if self.lock_delay_run:
            if self.lock_delay_times_left > 0:
                self.reset_lock_delay()
                if self.collision(self.current_posx, self.current_posy+1, self.current_id, self.current_spin_id):
                    self.lock_delay_run = True
            else:
                self.lock_delay_frames = 0

    def move_side(self, x_change):
        if self.current_id is not None and not self.collision(self.current_posx + x_change, self.current_posy, self.current_id, self.current_spin_id):
            self.current_posx += x_change
            if self.lock_delay_run:
                if self.lock_delay_times_left > 0:
                    self.reset_lock_delay()
                    if self.collision(self.current_posx, self.current_posy+1, self.current_id, self.current_spin_id):
                        self.lock_delay_run = True
                else:
                    self.lock_delay_frames = 1
            self.spin_is_last_move = False

    def save_state(self):
        k1 = self.current_posx
        if self.current_id is not None:
            i1 = self.current_posy
            for i in self.TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k:
                        self.FIELD[i1][k1] = k
                    k1 += 1
                k1 = self.current_posx
                i1 += 1
        self.pieces[self.current_id] += 1
        if len(self.garbage_queue) > 0:
            garbage_row = [None, Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30)), Block((30, 30, 30))]
            random.shuffle(garbage_row)
            for i in range(self.garbage_queue[0]):
                self.FIELD.append(garbage_row)
                self.FIELD.remove(self.FIELD[0])
            self.garbage_queue.remove(self.garbage_queue[0])

    def ghost_piece_y(self):
        y = self.current_posy
        while not self.collision(self.current_posx, y + 1, self.current_id,
                                 self.current_spin_id):
            y += 1
        return y

    def reset_lock_delay(self):
        self.lock_delay_frames = self.lock_delay_f_limit
        self.lock_delay_run = False
        self.lock_delay_times_left -= 1

    def move_down(self, instant=False):
        if self.current_id is not None and not self.collision(self.current_posx, self.current_posy + 1, self.current_id, self.current_spin_id):
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
                if self.soft_drop:
                    self.score[0] += 1
            return True
        else:
            return False

    def bot_move(self):
        bot_move = self.player.run_ai(self)
        if bot_move == "S+":
            self.spin()
        elif bot_move == "R":
            self.move_side(1)
        elif bot_move == "L":
            self.move_side(-1)
        elif bot_move == "HD":
            self.move_down(True)
            self.save_state()
            self.clear_lines()
            self.spawn_tetromino()
            self.lock_delay_run = False
            self.lock_delay_frames = 30
            self.lock_delay_times_left = 15


    def draw_game(self):
        win.fill((25, 25, 25))
        pygame.draw.rect(win, (0, 0, 0),
                         (130, (BLOCK_SIZE * 2 + 5), BLOCK_SIZE * 10, BLOCK_SIZE * 20))
        x = 0
        y = -self.buffer_y
        for i in self.FIELD:
            for k in i:
                window_x = 130 + BLOCK_SIZE * x
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
            for i in self.TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k is not None:
                        window_x = 130 + BLOCK_SIZE * k1
                        window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                        try:
                            pygame.draw.rect(win, (int(k.color[0]*self.lock_delay_frames/max(self.lock_delay_f_limit, 1)), int(k.color[1]*self.lock_delay_frames/max(self.lock_delay_f_limit, 1)), int(k.color[2]*self.lock_delay_frames/max(self.lock_delay_f_limit, 1))), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                        except ValueError:
                            pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                    k1 += 1
                k1 = self.current_posx
                i1 += 1
            if self.support_ghost_piece:
                i1 = self.ghost_piece_y() - self.buffer_y
                k1 = self.current_posx
                for i in self.TETROMINOS[self.current_id][self.current_spin_id]:
                    for k in i:
                        if k is not None:
                            window_x = 130 + BLOCK_SIZE * k1
                            window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                            pygame.draw.rect(win, (k.color[0], k.color[1], k.color[2]), (window_x+5, window_y+5, BLOCK_SIZE-10, BLOCK_SIZE-10), width=5, border_radius=1)
                        k1 += 1
                    k1 = self.current_posx
                    i1 += 1
        y_offset = 0
        win.blit(SMALL_FONT.render(f"{self.seed}", 1, (255, 255, 255)), (430, 30))
        win.blit(SMALL_FONT.render(f"#{sum(self.pieces)}", 1, (255, 255, 255)), (430, 45))
        for q in range(0, self.next_length):
            i1 = 0
            k1 = 0
            for i in self.TETROMINOS[self.next_queue[q]][0]:
                for k in i:
                    if k is not None:
                        window_x = 470 + 25 * k1
                        window_y = 65 + 25 * i1 + y_offset
                        pygame.draw.rect(win, k.color, (window_x, window_y, 25, 25))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25), width=2)
                    k1 += 1
                k1 = 0
                i1 += 1
            y_offset += 60
        if self.support_hold:
            if self.hold_id is not None:
                i1 = 0
                k1 = 0
                for i in self.TETROMINOS[self.hold_id][0]:
                    for k in i:
                        if k is not None:
                            window_x = 20 + 25 * k1
                            window_y = 65 + 25 * i1
                            if self.hold_locked:
                                pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25))
                            else:
                                pygame.draw.rect(win, k.color, (window_x, window_y, 25, 25))
                            pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25), width=1)
                        k1 += 1
                    k1 = 0
                    i1 += 1
        win.blit(MEDIUM_FONT.render("SCORE", 1, (255, 255, 255)), (440, 562))
        win.blit(MEDIUM_FONT.render(f"{sum(self.score):5d}", 1, (255, 255, 255)), (440, 582))
        win.blit(MEDIUM_FONT.render("LINES", 1, (255, 255, 255)), (440, 622))
        win.blit(MEDIUM_FONT.render(f"{sum(self.cleared_lines):5d}", 1, (255, 255, 255)), (440, 642))
        win.blit(MEDIUM_FONT.render("LV", 1, (255, 255, 255)), (80, 502))
        win.blit(MEDIUM_FONT.render(f"{self.level:02d}", 1, (255, 255, 255)), (80, 522))
        win.blit(MEDIUM_FONT.render("PPS", 1, (255, 255, 255)), (60, 562))
        try:
            pps = sum(self.pieces) / self.game_time
        except ZeroDivisionError:
            pps = 0
        win.blit(MEDIUM_FONT.render(f"{pps:6.2f}", 1, (255, 255, 255)), (0, 582))
        win.blit(MEDIUM_FONT.render("TIME", 1, (255, 255, 255)), (40, 622))
        win.blit(MEDIUM_FONT.render(f"{strfdelta(datetime.timedelta(seconds=self.game_time), '%m:%S'):>6s}", 1, (255, 255, 255)), (0, 642))
        if self.mode > 0:
            if self.mode == 1:
                win.blit(MEDIUM_FONT.render("TIME", 1, (255, 255, 255)), (440, 482))
                win.blit(MEDIUM_FONT.render(f"{strfdelta(datetime.timedelta(seconds=self.target), '%m:%S')}", 1, (255, 255, 255)), (440, 522))
            elif self.mode == 2:
                win.blit(MEDIUM_FONT.render("LINES", 1, (255, 255, 255)), (440, 482))
                win.blit(MEDIUM_FONT.render(f"{self.target:5d}", 1, (255, 255, 255)), (440, 522))
            win.blit(MEDIUM_FONT.render("LEFT", 1, (255, 255, 255)), (440, 502))

        if self.notification['for_what'] is not None and self.notification['game_time']+2.9 >= self.game_time:
            if self.notification['pc']:
                win.blit(FONT.render(self.for_what_score[self.notification['for_what']]+" PERFECT CLEAR", 1, (230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25)),
                     (300-int(FONT.size(self.for_what_score[self.notification['for_what']]+" PERFECT CLEAR")[0]/2), 670))
            else:
                win.blit(FONT.render(self.for_what_score[self.notification['for_what']], 1, (230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25)),
                     (300-int(FONT.size(self.for_what_score[self.notification['for_what']])[0]/2), 670))
            win.blit(
                FONT.render(f"+{self.notification['number']}", 1, (230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25, 230*(min(self.notification['game_time']+3-self.game_time, 1))+25)),
                (300-int(FONT.size(f"+{self.notification['number']}")[0]/2), 695))
            if self.notification["combo"] > 0:
                win.blit(
                    FONT.render(f"COMBO × {self.notification['combo']}", 1, (
                    230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25, 230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25,
                    230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25)),
                    (300-int(FONT.size(f"COMBO × {self.notification['combo']}")[0]/2), 720))
            if self.notification['b2b'] > 0:
                win.blit(
                    FONT.render(f"BACK-TO-BACK × {self.notification['b2b']}", 1, (
                    230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25, 230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25,
                    230 * (min(self.notification['game_time']+3-self.game_time, 1)) + 25)),
                    (300-int(FONT.size(f"BACK-TO-BACK × {self.notification['b2b']}")[0]/2), 745))
        if self.game_over:
            text_size_x = FONT.size("GAME")[0]
            pygame.draw.rect(win, (0, 0, 0), (223, 327, text_size_x+10, 60))
            if self.mode > 0 and self.target <= 0:
                pygame.draw.rect(win, (0, 255, 0), (223, 327, text_size_x + 10, 60), width=2)
                win.blit(FONT.render("WELL", 1, (255, 255, 255)), (230, 335))
                win.blit(FONT.render("DONE", 1, (255, 255, 255)), (230, 360))
            else:
                pygame.draw.rect(win, (255, 0, 0), (223, 327, text_size_x + 10, 60), width=2)
                win.blit(FONT.render("GAME", 1, (255, 255, 255)), (230, 335))
                win.blit(FONT.render("OVER", 1, (255, 255, 255)), (230, 360))
        pygame.display.update()

    def draw_game_stats(self):
        win.fill((25, 25, 25))
        if self.game_over:
            win.blit(FONT.render("STATISTIC", 1, (255, 255, 255)), (25, 25))
        else:
            win.blit(FONT.render("GAME PAUSED", 1, (255, 255, 255)), (25, 25))
        total_score = sum(self.score)
        win.blit(FONT.render(f"SCORE {total_score:16d}", 1, (255, 255, 255)), (25, 100))
        total_pieces = sum(self.pieces)
        win.blit(FONT.render(f"PIECES {total_pieces:15d}", 1, (255, 255, 255)), (25, 130))
        total_lines = sum(self.cleared_lines)
        win.blit(FONT.render(f"LINES {total_lines:16d}", 1, (255, 255, 255)), (25, 160))
        try:
            pps = total_pieces / self.game_time
        except ZeroDivisionError:
            pps = 0
        win.blit(FONT.render(f"PIECES PER SECOND {pps:0.2f}", 1, (255, 255, 255)), (25, 190))
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
        win.blit(SMALL_FONT.render(f"QUAD {tetris_times:7d} {self.cleared_lines[3]:5d}      I {self.pieces[5]:<10d}", 1, (255, 255, 255)),
                 (25, 355))
        win.blit(SMALL_FONT.render(f"SCORE TABLE", 1, (255, 255, 255)), (25, 380))
        win.blit(SMALL_FONT.render(f"SOFT DROPS {self.score[0]:14d}", 1, (255, 255, 255)), (25, 400))
        win.blit(SMALL_FONT.render(f"HARD DROPS {self.score[1]:14d}", 1, (255, 255, 255)), (25, 415))
        win.blit(SMALL_FONT.render(f"SINGLE {self.score[2]:18d}", 1, (255, 255, 255)), (25, 430))
        win.blit(SMALL_FONT.render(f"DOUBLE {self.score[3]:18d}", 1, (255, 255, 255)), (25, 445))
        win.blit(SMALL_FONT.render(f"TRIPLE {self.score[4]:18d}", 1, (255, 255, 255)), (25, 460))
        win.blit(SMALL_FONT.render(f"QUAD {self.score[5]:20d}", 1, (255, 255, 255)), (25, 475))
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


class ClassicTetris(TetrisGameplay):
    def __init__(self, mode=0, target=0, player="P1", seed=random.randint(-2147483648, 2147483647)):
        super().__init__(mode, target, 2, player, False, False, False, False, False, False, (267, 100), True, 1, seed)
        self.TETROMINOS = [
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
                    [None, None, None, None],
                    [Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240)), Block((0, 240, 240))],
                    [None, None, None, None]
                ],
                [
                    [None, None, Block((0, 240, 240)), None],
                    [None, None, Block((0, 240, 240)), None],
                    [None, None, Block((0, 240, 240)), None],
                    [None, None, Block((0, 240, 240)), None]
                ]
            ],  # 5, I
            [
                [
                    [Block((255, 240, 0)), Block((255, 240, 0)), None, None],
                    [Block((255, 240, 0)), Block((255, 240, 0)), None, None],
                    [None, None, None, None],
                    [None, None, None, None]
                ]
            ]  # 6, O
        ]

    def __str__(self):
        ans = f"size_x={len(self.FIELD[0])}, size_y={len(self.FIELD)}, Field:"
        for i in self.FIELD:
            ans += f"\n{i}"
        return ans

    def gravity_and_lines_table(self):
        if self.level == 0:
            return 1/48, 10
        elif self.level == 1:
            return 1/43, 20
        elif self.level == 2:
            return 1/38, 30
        elif self.level == 3:
            return 1/33, 40
        elif self.level == 4:
            return 1/28, 50
        elif self.level == 5:
            return 1/23, 60
        elif self.level == 6:
            return 1/18, 70
        elif self.level == 7:
            return 1/13, 80
        elif self.level == 8:
            return 1/8, 90
        elif self.level == 9:
            return 1/6, 100
        elif 10 <= self.level <= 12:
            return 1/5, 100
        elif 13 <= self.level <= 15:
            return 1/4, 100
        elif self.level == 16:
            return 1/3, 110
        elif self.level == 17:
            return 1/3, 120
        elif self.level == 18:
            return 1/3, 130
        elif self.level == 19:
            return 1/2, 140
        elif self.level == 20:
            return 1/2, 150
        elif self.level == 21:
            return 1/2, 160
        elif self.level == 22:
            return 1/2, 170
        elif self.level == 23:
            return 1/2, 180
        elif self.level == 24:
            return 1/2, 190
        elif 25 <= self.level <= 28:
            return 1/2, 200
        else:
            return 1, 200

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
            if ic == 10:
                cleared += 1
                self.FIELD.remove(i)
                new = list(range(10))
                x = 0
                while x != 10:
                    new[x] = None
                    x += 1
                self.FIELD.insert(0, new)
            y -= 1
            if ic > 0 and height is None:
                height = y
                frames_delay += 10 + (2 * int(height / 4))

        if cleared > 0:
            self.cleared_lines[cleared - 1] += cleared
            if self.mode == 2:
                self.target -= cleared
                if self.target <= 0:
                    self.target = 0
                    self.game_over = True
            frames_delay += 18
            self.score_up = 0
            self.for_what_delay = 3
            if cleared == 1:
                self.score[2] += 40 * (min(self.level, 29) + 1)
                self.score_up += 40 * (min(self.level, 29) + 1)
                self.for_what_id = 0
            elif cleared == 2:
                self.score[3] += 100 * (min(self.level, 29) + 1)
                self.score_up += 100 * (min(self.level, 29) + 1)
                self.for_what_id = 1
            elif cleared == 3:
                self.score[4] += 300 * (min(self.level, 29) + 1)
                self.score_up += 300 * (min(self.level, 29) + 1)
                self.for_what_id = 2
            elif cleared == 4:
                self.score[5] += 1200 * (min(self.level, 29) + 1)
                self.score_up += 1200 * (min(self.level, 29) + 1)
                self.for_what_id = 3
            if sum(self.cleared_lines) >= self.lines_for_level_up:
                self.level += 1
                self.lines_for_level_up += 10
        return frames_delay

    def draw_game(self):
        win.fill((25, 25, 25))
        pygame.draw.rect(win, (0, 0, 0),
                         (130, (BLOCK_SIZE * 2 + 5), BLOCK_SIZE * 10, BLOCK_SIZE * 20))
        x = 0
        y = -self.buffer_y
        for i in self.FIELD:
            for k in i:
                window_x = 130 + BLOCK_SIZE * x
                window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * y
                if k is not None:
                    pygame.draw.rect(win, k.color, (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                x += 1
            x = 0
            y += 1
        i1 = self.current_posy - self.buffer_y
        k1 = self.current_posx
        if self.current_id is not None:
            for i in self.TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k is not None:
                        window_x = 130 + BLOCK_SIZE * k1
                        window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                        pygame.draw.rect(win, (int(k.color[0]*self.lock_delay_frames/30), int(k.color[1]*self.lock_delay_frames/30), int(k.color[2]*self.lock_delay_frames/30)), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                    k1 += 1
                k1 = self.current_posx
                i1 += 1
        x_offset = 0
        win.blit(SMALL_FONT.render(f"{self.seed}", 1, (255, 255, 255)), (430, 30))
        win.blit(SMALL_FONT.render(f"#{sum(self.pieces)}", 1, (255, 255, 255)), (430, 45))
        for q in range(0, self.next_length):
            i1 = 0
            k1 = 0
            for i in self.TETROMINOS[self.next_queue[q]][0]:
                for k in i:
                    if k is not None:
                        window_x = 130 + BLOCK_SIZE * 10 + 20 + BLOCK_SIZE * k1 + x_offset
                        window_y = (BLOCK_SIZE * 2 + 30) + BLOCK_SIZE * i1
                        pygame.draw.rect(win, k.color, (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=1)
                    k1 += 1
                k1 = 0
                i1 += 1
            x_offset += 45
        if self.support_hold:
            if self.hold_id is not None:
                i1 = 0
                k1 = 0
                for i in self.TETROMINOS[self.hold_id][0]:
                    for k in i:
                        if k is not None:
                            window_x = 10 + BLOCK_SIZE * k1
                            window_y = (BLOCK_SIZE * 2 + 30) + 10 * i1
                            pygame.draw.rect(win, k.color, (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                            pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=1)
                        k1 += 1
                    k1 = 0
                    i1 += 1
        win.blit(MEDIUM_FONT.render("SCORE", 1, (255, 255, 255)), (440, 562))
        win.blit(MEDIUM_FONT.render(f"{sum(self.score):5d}", 1, (255, 255, 255)), (440, 582))
        win.blit(MEDIUM_FONT.render("LINES", 1, (255, 255, 255)), (440, 622))
        win.blit(MEDIUM_FONT.render(f"{sum(self.cleared_lines):5d}", 1, (255, 255, 255)), (440, 642))
        win.blit(MEDIUM_FONT.render("LV", 1, (255, 255, 255)), (80, 502))
        win.blit(MEDIUM_FONT.render(f"{self.level:02d}", 1, (255, 255, 255)), (80, 522))
        win.blit(MEDIUM_FONT.render("TRT", 1, (255, 255, 255)), (60, 562))
        try:
            tetris_rate = int((self.cleared_lines[3] / sum(self.cleared_lines)) * 100)
        except ZeroDivisionError:
            tetris_rate = 0
        if tetris_rate == 100:
            win.blit(MEDIUM_FONT.render(f"{tetris_rate}", 1, (255, 255, 255)), (60, 582))
        else:
            win.blit(MEDIUM_FONT.render(f"{tetris_rate:02d}%", 1, (255, 255, 255)), (60, 582))
        win.blit(MEDIUM_FONT.render("TIME", 1, (255, 255, 255)), (40, 622))
        win.blit(MEDIUM_FONT.render(f"{strfdelta(datetime.timedelta(seconds=self.game_time), '%m:%S'):>6s}", 1, (255, 255, 255)), (0, 642))
        if self.mode > 0:
            if self.mode == 1:
                win.blit(MEDIUM_FONT.render("TIME", 1, (255, 255, 255)), (440, 482))
                win.blit(MEDIUM_FONT.render(f"{strfdelta(datetime.timedelta(seconds=self.target), '%m:%S')}", 1, (255, 255, 255)), (440, 522))
            elif self.mode == 2:
                win.blit(MEDIUM_FONT.render("LINES", 1, (255, 255, 255)), (440, 482))
                win.blit(MEDIUM_FONT.render(f"{self.target:5d}", 1, (255, 255, 255)), (440, 522))
            win.blit(MEDIUM_FONT.render("LEFT", 1, (255, 255, 255)), (440, 502))
        if self.notification['for_what'] is not None and self.notification['game_time'] + 2.9 >= self.game_time:
            win.blit(FONT.render(self.for_what_score[self.notification['for_what']], 1, (
            230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
            230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
            230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25)),
                     (300 - int(FONT.size(self.for_what_score[self.notification['for_what']])[0] / 2), 670))
            win.blit(
                FONT.render(f"+{self.notification['number']}", 1, (
                230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25)),
                (300 - int(FONT.size(f"+{self.notification['number']}")[0] / 2), 695))
            if self.notification["combo"] > 0:
                win.blit(
                    FONT.render(f"COMBO × {self.notification['combo']}", 1, (
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25)),
                    (300 - int(FONT.size(f"COMBO × {self.notification['combo']}")[0] / 2), 720))
            if self.notification['b2b'] > 0:
                win.blit(
                    FONT.render(f"BACK-TO-BACK × {self.notification['b2b']}", 1, (
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25,
                        230 * (min(self.notification['game_time'] + 3 - self.game_time, 1)) + 25)),
                    (300 - int(FONT.size(f"BACK-TO-BACK × {self.notification['b2b']}")[0] / 2), 745))
        if self.game_over:
            text_size_x = FONT.size("GAME")[0]
            pygame.draw.rect(win, (0, 0, 0), (223, 327, text_size_x + 10, 60))
            if self.mode > 0 and self.target <= 0:
                pygame.draw.rect(win, (0, 255, 0), (223, 327, text_size_x + 10, 60), width=2)
                win.blit(FONT.render("WELL", 1, (255, 255, 255)), (230, 335))
                win.blit(FONT.render("DONE", 1, (255, 255, 255)), (230, 360))
            else:
                pygame.draw.rect(win, (255, 0, 0), (223, 327, text_size_x + 10, 60), width=2)
                win.blit(FONT.render("GAME", 1, (255, 255, 255)), (230, 335))
                win.blit(FONT.render("OVER", 1, (255, 255, 255)), (230, 360))
        pygame.display.update()

    def draw_game_stats(self):
        win.fill((25, 25, 25))
        if self.game_over:
            win.blit(FONT.render("STATISTIC", 1, (255, 255, 255)), (25, 25))
        else:
            win.blit(FONT.render("GAME PAUSED", 1, (255, 255, 255)), (25, 25))
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
        win.blit(FONT.render(f"QUAD RATE {tetris_rate:12.2%}", 1, (255, 255, 255)), (25, 190))
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
        win.blit(SMALL_FONT.render(f"QUAD {tetris_times:7d} {self.cleared_lines[3]:5d}      I {self.pieces[5]:<10d}", 1, (255, 255, 255)),
                 (25, 355))
        win.blit(SMALL_FONT.render(f"SCORE TABLE", 1, (255, 255, 255)), (25, 380))
        win.blit(SMALL_FONT.render(f"DROPS {self.score[0]:7d}", 1, (255, 255, 255)), (25, 400))
        win.blit(SMALL_FONT.render(f"SINGLE {self.score[2]:6d}", 1, (255, 255, 255)), (25, 415))
        win.blit(SMALL_FONT.render(f"DOUBLE {self.score[3]:6d}", 1, (255, 255, 255)), (25, 430))
        win.blit(SMALL_FONT.render(f"TRIPLE {self.score[4]:6d}", 1, (255, 255, 255)), (25, 445))
        win.blit(SMALL_FONT.render(f"QUAD {self.score[5]:8d}", 1, (255, 255, 255)), (25, 460))
        pygame.display.update()


class BotAI:
    def __init__(self):
        self.skill = 0
        self.name = "Bot"
        self.state = "idle"
        self.selected_move = (None, None) # rot, pos

    def holes_and_wells(self, board):
        pass

    def generate_moves(self, field):
        test_spin_id = 0
        test_mino_id = field.current_id
        test_hold_mino_id = field.hold_id if field.hold_id else field.next_queue[0]
        moves = []
        while test_spin_id < len(field.TETROMINOS[test_mino_id]):
            x = 0
            while x < len(field.FIELD[0]):
                if not field.collision(x, 0, test_mino_id, test_spin_id):
                    y = field.current_posy
                    while not field.collision(x, y + 1, test_mino_id, test_spin_id):
                        y += 1
                    moves.append((test_spin_id, x, y, False))
                x += 1
            test_spin_id += 1
        test_spin_id = 0
        while test_spin_id < len(field.TETROMINOS[test_hold_mino_id]):
            x = 0
            while x < len(field.FIELD[0]):
                if not field.collision(x, 0, test_hold_mino_id, test_spin_id):
                    y = field.current_posy
                    while not field.collision(x, y + 1, test_hold_mino_id, test_spin_id):
                        y += 1
                    moves.append((test_spin_id, x, y, True))
                x += 1
            test_spin_id += 1
        answer = random.choice(moves)
        return answer[0], answer[1]


    def run_ai(self, field):
        pass
        # if self.selected_move == (None, None):
        #     self.selected_move = self.generate_moves(field)
        #     print(self.selected_move)
        # if field.current_spin_id != self.selected_move[0] and field.current_id != 6:
        #     return "S+"
        # elif field.current_posx < self.selected_move[1]:
        #     return "R"
        # elif field.current_posx > self.selected_move[1]:
        #     return "L"
        # else:
        #     self.selected_move = (None, None)
        #     return "HD"



def draw_main_menu(selected, sel_gl, sel_md, sel_trg):
    win.fill((25, 25, 25))
    win.blit(FONT.render("PYTRIS by dan63047", 1, (255, 255, 255)), (25, 25))
    win.blit(FONT.render("›", 1, (255, 255, 255)), (25, 100 + 30 * selected))
    win.blit(FONT.render("Start", 1, (255, 255, 255)), (50, 100))
    win.blit(FONT.render(f"Mode: {MODES[sel_md]}", 1, (255, 255, 255)), (50, 130))
    if sel_md == 0:
        win.blit(FONT.render(f"Level: {sel_trg:02d}", 1, (255, 255, 255)), (50, 160))  # ↑↓
    elif sel_md == 1:
        win.blit(FONT.render(f"Time: {strfdelta(datetime.timedelta(seconds=TIME_LIMITS_SEC[sel_trg]), '%H:%M:%S.%Z')}", 1, (255, 255, 255)), (50, 160))
    elif sel_md == 2:
        win.blit(FONT.render(f"Lines: {LINES_LIMITS[sel_trg]}", 1, (255, 255, 255)), (50, 160))
    win.blit(FONT.render(f"Guideline: {GUIDELINES[sel_gl]}", 1, (255, 255, 255)), (50, 190))
    win.blit(FONT.render(f"Exit", 1, (255, 255, 255)), (50, 220))
    pygame.display.update()

def mind_of_stupid_idiot():
    while not session[1].game_over:
        try:
            session[1].bot_move()
            time.sleep(0.25)
        except IndexError:
            time.sleep(1)
        except Exception as e:
            print(e)
    
def draw_vs_field(field, offset, size=30):
    pygame.draw.rect(win, (0, 0, 0), (offset + 100, (BLOCK_SIZE * 2 + 5), BLOCK_SIZE * 10, BLOCK_SIZE * 20))
    x = 0
    y = -field.buffer_y
    for i in field.FIELD:
        for k in i:
            window_x = offset + 100 + BLOCK_SIZE * x
            window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * y
            if k is not None:
                pygame.draw.rect(win, k.color, (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
            else:
                pygame.draw.rect(win, (25, 25, 25), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=1)
            x += 1
        x = 0
        y += 1
    i1 = field.current_posy - field.buffer_y
    k1 = field.current_posx
    if field.current_id is not None:
        for i in field.TETROMINOS[field.current_id][field.current_spin_id]:
            for k in i:
                if k is not None:
                    window_x = offset + 100 + BLOCK_SIZE * k1
                    window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                    pygame.draw.rect(win, (
                        int(k.color[0] * field.lock_delay_frames / max(field.lock_delay_f_limit, 1)),
                        int(k.color[1] * field.lock_delay_frames / max(field.lock_delay_f_limit, 1)),
                        int(k.color[2] * field.lock_delay_frames / max(field.lock_delay_f_limit, 1))),
                                     (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE), width=2)
                k1 += 1
            k1 = field.current_posx
            i1 += 1
        if field.support_ghost_piece:
            i1 = field.ghost_piece_y() - field.buffer_y
            k1 = field.current_posx
            for i in field.TETROMINOS[field.current_id][field.current_spin_id]:
                for k in i:
                    if k is not None:
                        window_x = offset + 100 + BLOCK_SIZE * k1
                        window_y = (BLOCK_SIZE * 2 + 5) + BLOCK_SIZE * i1
                        pygame.draw.rect(win, (k.color[0], k.color[1], k.color[2]),
                                         (window_x + 5, window_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10),
                                         width=5, border_radius=1)
                    k1 += 1
                k1 = field.current_posx
                i1 += 1
    y_offset = 0
    for q in range(field.next_length):
        k1 = 0
        for i1, i in enumerate(field.TETROMINOS[field.next_queue[q]][0]):
            for k in i:
                if k is not None:
                    window_x = offset + 440 + 25 * k1
                    window_y = 65 + 25 * i1 + y_offset
                    pygame.draw.rect(win, k.color, (window_x, window_y, 25, 25))
                    pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25), width=2)
                k1 += 1
            k1 = 0
        y_offset += 60
    garbage_meter_y_offset = 640
    garbage_meter_color = (255, 0, 0)
    for g in field.garbage_queue:
        for i in range(g):
            window_y = garbage_meter_y_offset
            pygame.draw.rect(win, garbage_meter_color, (offset + 60, window_y, 30, 30), width=2)
            garbage_meter_y_offset -= 30
        garbage_meter_color = (255, 120, 0)
        garbage_meter_y_offset -= 5
    if field.support_hold and field.hold_id is not None:
        k1 = 0
        for i1, i in enumerate(field.TETROMINOS[field.hold_id][0]):
            for k in i:
                if k is not None:
                    window_x = offset + 20 + 25 * k1
                    window_y = 30 + 25 * i1
                    if field.hold_locked:
                        pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25))
                    else:
                        pygame.draw.rect(win, k.color, (window_x, window_y, 25, 25))
                    pygame.draw.rect(win, (0, 0, 0), (window_x, window_y, 25, 25), width=1)
                k1 += 1
            k1 = 0
    try:
        pps = sum(field.pieces) / field.game_time
    except ZeroDivisionError:
        pps = 0
    try:
        apm = field.attack / (field.game_time / 60)
    except ZeroDivisionError:
        apm = 0
    win.blit(MEDIUM_FONT.render(f"{pps:.2f} PPS", 1, (255, 255, 255)), (offset + 410, 522))
    win.blit(MEDIUM_FONT.render(f"{sum(field.pieces)} P", 1, (255, 255, 255)), (offset + 410, 542))
    win.blit(MEDIUM_FONT.render(strfdelta(datetime.timedelta(seconds=field.game_time), '%m:%S'), 1, (255, 255, 255)), (offset + 410, 502))
    win.blit(MEDIUM_FONT.render(f"{apm:.0f} APM", 1, (255, 255, 255)), (offset + 410, 562))
    win.blit(MEDIUM_FONT.render(f"{field.attack} ATK", 1, (255, 255, 255)), (offset + 410, 582))
    if field.mode == 3:
        try:
            win.blit(MEDIUM_FONT.render(field.player, 1, (255, 255, 255)), (offset + 410, 482))
        except:
            win.blit(MEDIUM_FONT.render(field.player.name, 1, (255, 255, 255)), (offset + 410, 482))

    if field.notification['for_what'] is not None and field.notification['game_time'] + 2.9 >= field.game_time:
        win.blit(FONT.render(field.for_what_score[field.notification['for_what']], 1, (
        230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
        230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
        230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25)),
                 (300 - int(FONT.size(field.for_what_score[field.notification['for_what']])[0] / 2), 670))
        win.blit(
            FONT.render(f"+{field.notification['number']}", 1, (
            230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
            230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
            230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25)),
            (300 - int(FONT.size(f"+{field.notification['number']}")[0] / 2), 695))
        if field.notification["combo"] > 0:
            win.blit(
                FONT.render(f"COMBO × {field.notification['combo']}", 1, (
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25)),
                (300 - int(FONT.size(f"COMBO × {field.notification['combo']}")[0] / 2), 720))
        if field.notification['b2b'] > 0:
            win.blit(
                FONT.render(f"BACK-TO-BACK × {field.notification['b2b']}", 1, (
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25,
                    230 * (min(field.notification['game_time'] + 3 - field.game_time, 1)) + 25)),
                (300 - int(FONT.size(f"BACK-TO-BACK × {field.notification['b2b']}")[0] / 2), 745))
    if field.game_over:
        text_size_x = FONT.size("GAME")[0]
        pygame.draw.rect(win, (0, 0, 0), (offset + 223, 327, text_size_x + 10, 60))
        if field.mode > 0 and field.target <= 0:
            pygame.draw.rect(win, (0, 255, 0), (offset + 223, 327, text_size_x + 10, 60), width=2)
            win.blit(FONT.render("WELL", 1, (255, 255, 255)), (offset + 230, 335))
            win.blit(FONT.render("DONE", 1, (255, 255, 255)), (offset + 230, 360))
        else:
            pygame.draw.rect(win, (255, 0, 0), (offset + 223, 327, text_size_x + 10, 60), width=2)
            win.blit(FONT.render("GAME", 1, (255, 255, 255)), (offset + 230, 335))
            win.blit(FONT.render("OVER", 1, (255, 255, 255)), (offset + 230, 360))

def draw_vs_gameplay(session):
    win.fill((25, 25, 25))
    for f in session:
        if f.player == "P1":
            draw_vs_field(f, 0)
        elif len(session) == 2 and f.player.name == "Bot":
            draw_vs_field(f, 600)
    pygame.display.update()

def render_main():
    while True:
        if state == "main menu":
            draw_main_menu(menu_select, selected_gl, selected_mode, selected_target)
        elif state == "gameplay":
            if selected_mode == 3:
                draw_vs_gameplay(session)
            else:
                session[0].draw_game()
        elif state == "gameplay_stats":
            session[0].draw_game_stats()


def main():
    GAME_RUN = True
    global session
    ticks_before_stats = 180
    global state
    global menu_select
    global selected_gl
    global selected_mode
    global selected_target
    delay_before_spawn = -1
    on_pause = False
    corrupted_keys = []
    field = None
    piece_movement = 0
    incoming_garbage = []
    first_movement = True
    render_tread = threading.Thread(name="drawing", target=render_main, daemon=True)
    render_tread.start()
    movement_delay = 0
    pygame.key.set_repeat(267, 100)
    while GAME_RUN:
        clock.tick(60)
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_movement = -1
                elif event.key == pygame.K_RIGHT:
                    piece_movement = 1
                pressed_keys.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and pygame.K_SPACE in corrupted_keys:
                    corrupted_keys.remove(pygame.K_SPACE)
                if event.key == pygame.K_DOWN and state == "gameplay":
                    corrupted_keys.append(pygame.K_DOWN)
                if event.key == pygame.K_UP and state == "gameplay" and pygame.K_UP in corrupted_keys:
                    corrupted_keys.remove(pygame.K_UP)
                if event.key == pygame.K_x and state == "gameplay" and pygame.K_x in corrupted_keys:
                    corrupted_keys.remove(pygame.K_x)
                if event.key == pygame.K_z and pygame.K_z in corrupted_keys:
                    corrupted_keys.remove(pygame.K_z)
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    piece_movement = 0
                    first_movement = True
                    try:
                        movement_delay = field.handling[0]
                    except:
                        pass
            for i in pressed_keys:
                if i in corrupted_keys:
                    pressed_keys.remove(i)
        keys = pygame.key.get_pressed()
        if state == "main menu":
            if pygame.K_RETURN in pressed_keys and menu_select == 0:
                state = "pregameplay"
            if pygame.K_DOWN in pressed_keys and menu_select != 4:
                menu_select += 1
            if pygame.K_UP in pressed_keys and menu_select != 0:
                menu_select -= 1
            if pygame.K_RIGHT in pressed_keys and selected_mode != 3 and menu_select == 1:
                selected_mode += 1
                selected_target = 0
            elif pygame.K_LEFT in pressed_keys and selected_mode != 0 and menu_select == 1:
                selected_mode -= 1
                selected_target = 0
            if selected_mode == 0:
                if pygame.K_RIGHT in pressed_keys and menu_select == 2 and selected_target != 30:
                    selected_target += 1
                elif pygame.K_LEFT in pressed_keys and menu_select == 2 and selected_target != 0:
                    selected_target -= 1
            elif selected_mode == 1:
                if pygame.K_RIGHT in pressed_keys and menu_select == 2 and selected_target != len(TIME_LIMITS_SEC)-1:
                    selected_target += 1
                elif pygame.K_LEFT in pressed_keys and menu_select == 2 and selected_target != 0:
                    selected_target -= 1
            elif selected_mode == 2:
                if pygame.K_RIGHT in pressed_keys and menu_select == 2 and selected_target != len(LINES_LIMITS)-1:
                    selected_target += 1
                elif pygame.K_LEFT in pressed_keys and menu_select == 2 and selected_target != 0:
                    selected_target -= 1
            if pygame.K_RIGHT in pressed_keys and selected_gl != 1 and menu_select == 3:
                selected_gl += 1
            elif pygame.K_LEFT in pressed_keys and selected_gl != 0 and menu_select == 3:
                selected_gl -= 1
            if pygame.K_RETURN in pressed_keys and menu_select == 4:
                GAME_RUN = False
        elif state == "pregameplay":
            ticks_before_stats = 300
            delay_before_spawn = -1
            seed = random.randint(-2147483648, 2147483647)
            if selected_gl == 0:
                session = [TetrisGameplay(selected_mode, max(selected_target, 1), seed=seed)] if selected_mode == 0 else [TetrisGameplay(selected_mode, selected_target, seed=seed)]
                if selected_mode == 3:
                    session.append(TetrisGameplay(selected_mode, selected_target, player=BotAI(), seed=seed))
                    bots_tread = threading.Thread(name="pendehos", target=mind_of_stupid_idiot, daemon=True)
                    bots_tread.start()
                    pygame.display.set_mode((1200, 800))
            elif selected_gl == 1:
                session = [ClassicTetris(selected_mode, selected_target, seed=seed)]
                if selected_mode == 3:
                    session.append(ClassicTetris(selected_mode, selected_target, BotAI(), seed=seed))
                    bots_tread = threading.Thread(name="pendehos", target=mind_of_stupid_idiot, daemon=True)
                    bots_tread.start()
                    pygame.display.set_mode((1200, 800))
            pygame.key.set_repeat(session[0].handling[0], session[0].handling[1])
            movement_delay = session[0].handling[0]
            state = "gameplay"
        elif state == "gameplay":
            field = session[0]
            frame_time = clock.get_time()/1000
            if not field.game_over:
                if field.player == "P1":
                    if pygame.K_r in pressed_keys:
                        state = "pregameplay"
                    if pygame.K_p in pressed_keys:
                        on_pause = True
                        state = "gameplay_stats"
                    if pygame.K_UP in pressed_keys:
                        field.spin()
                        corrupted_keys.append(pygame.K_UP)
                    if pygame.K_x in pressed_keys:
                        field.spin()
                        corrupted_keys.append(pygame.K_x)
                    if pygame.K_z in pressed_keys:
                        field.spin(True)
                        corrupted_keys.append(pygame.K_z)
                    if pygame.K_c in pressed_keys and field.support_hold and not field.hold_locked:
                        field.hold_tetromino()
                    if pygame.K_DOWN in pressed_keys:
                        field.soft_drop = True
                    if pygame.K_DOWN in corrupted_keys:
                        field.soft_drop = False
                        corrupted_keys.remove(pygame.K_DOWN)
                    if pygame.K_SPACE in pressed_keys and field.can_hard_drop:
                        field.move_down(True)
                        _extracted_from_main_136(field, incoming_garbage)
                        field.lock_delay_run = False
                        field.lock_delay_frames = 30
                        corrupted_keys.append(pygame.K_SPACE)
                    if piece_movement != 0:
                        movement_delay -= frame_time * 1000
                        if first_movement:
                            field.move_side(piece_movement)
                            first_movement = False
                        elif movement_delay <= 0:
                            field.move_side(piece_movement)
                            movement_delay = field.handling[1]
                for field in session:
                    field.game_time += frame_time
                    for gb in incoming_garbage:
                        if gb[1] != field.player:
                            field.garbage_queue.append(gb[0])
                            incoming_garbage.remove(gb)
                    if field.mode == 1:
                        field.target -= frame_time
                        if field.target <= 0:
                            field.target = 0
                            field.game_over = True
                    elif field.mode == 3 and field.target == 0:
                        field.game_over = True
                    if not field.game_over:
                        field.g += field.gravity_and_lines_table()[0]
                        if field.soft_drop:
                            field.g += field.soft_drop_speed
                        field.g = min(field.g, 22)
                        while field.g >= 1:
                            if field.support_lock_delay:
                                if not field.move_down() or field.collision(field.current_posx, field.current_posy+1, field.current_id, field.current_spin_id):
                                    field.lock_delay_run = True
                            elif (
                                not field.move_down()
                                and delay_before_spawn == -1
                            ):
                                field.save_state()
                                delay_before_spawn = field.clear_lines()
                                field.current_id = None
                            field.g -= 1
                        if field.nes_mechanics:
                            if delay_before_spawn > -1:
                                delay_before_spawn -= 1
                            if delay_before_spawn == 0:
                                field.spawn_tetromino()
                    if field.lock_delay_run:
                        if field.lock_delay_frames > 0:
                            field.lock_delay_frames -= 1
                        if (field.lock_delay_frames == 0 or not field.support_lock_delay) and field.collision(field.current_posx, field.current_posy+1, field.current_id, field.current_spin_id):
                            _extracted_from_main_136(field, incoming_garbage)
                            field.reset_lock_delay()
                            field.reset_lock_delay()
            for field in session:
                if field.game_over:
                    if field.player == "P1":
                        ticks_before_stats -= 1
                    elif field.mode == 3:
                        session[0].target -= 1
                    if ticks_before_stats <= 0:
                        state = "gameplay_stats"
        elif state == "gameplay_stats":
            if pygame.K_BACKSPACE in pressed_keys:
                pygame.key.set_repeat(267, 100)
                pygame.display.set_mode((600, 800))
                state = "main menu"
            elif pygame.K_r in pressed_keys:
                state = "pregameplay"
            if pygame.K_p in pressed_keys and not session[0].game_over:
                on_pause = False
                state = "gameplay"

def _extracted_from_main_136(field, ig):
    field.save_state()
    if field.mode == 3:
        atk =field.clear_lines()[1]
        if atk > 0:
            ig.append([atk, field.player])
    else:
        field.clear_lines()    
    field.spawn_tetromino()


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((600, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption("dan63047 Tetris")
    pygame.font.init()
    FONT = pygame.font.Font("PressStart2P-vaV7.ttf", 25)
    MEDIUM_FONT = pygame.font.Font("PressStart2P-vaV7.ttf", 20)
    SMALL_FONT = pygame.font.Font("PressStart2P-vaV7.ttf", 15)
    main()
    pygame.quit()
