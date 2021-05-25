from typing import List

import pygame, random, datetime
from string import Template

BLOCK_SIZE = 30
GUIDELINES = ["Current", "NES like"]


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
    d["m"] = minutes
    return t.substitute(**d)


class TetrisGameplay:
    def __init__(self, level=0, buffer_zone=20, srs=True, lock_delay=True, seven_bag=True, ghost_piece=True, hold=True, hard_drop=True, handling=(167, 33), nes_mechanics=False, next_len=4):
        self.buffer_y = buffer_zone
        self.FIELD = list(range(20 + buffer_zone))
        y = 0
        while y != len(self.FIELD):
            self.FIELD[y] = list(range(10))
            x = 0
            while x != 10:
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
        self.current_posx = 4
        self.current_posy = self.buffer_y - 2
        self.can_hard_drop = hard_drop
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
        self.for_what_delay = 0
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
        self.lock_delay_run = False
        self.lock_delay_frames = 30
        self.level = level
        self.lines_for_level_up = self.gravity_and_lines_table()[1]
        self.start_level = level
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

    def gravity_and_lines_table(self):
        return 1 / (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1) * 0.016666, self.level * 10 + 10

    def clear_lines(self):
        cleared = 0
        difficult = False
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

        if cleared > 0:
            self.cleared_lines[cleared - 1] += cleared
            self.combo += 1
            self.score_up = 0
            if t_spin:
                difficult = True
                if cleared == 1:
                    self.score[10] += 800 * (min(self.level, 29) + 1)
                    self.score_up += 800 * (min(self.level, 29) + 1)
                    self.for_what_id = 8
                elif cleared == 2:
                    self.score[11] += 1200 * (min(self.level, 29) + 1)
                    self.score_up += 1200 * (min(self.level, 29) + 1)
                    self.for_what_id = 9
                elif cleared == 3:
                    self.score[12] += 1600 * (min(self.level, 29) + 1)
                    self.score_up += 1600 * (min(self.level, 29) + 1)
                    self.for_what_id = 10
            elif t_spin_mini:
                difficult = True
                if cleared == 1:
                    self.score[7] += 200 * (min(self.level, 29) + 1)
                    self.score_up += 200 * (min(self.level, 29) + 1)
                    self.for_what_id = 5
                elif cleared == 2:
                    self.score[8] += 400 * (min(self.level, 29) + 1)
                    self.score_up += 400 * (min(self.level, 29) + 1)
                    self.for_what_id = 6
            else:
                if cleared == 1:
                    self.score[2] += 100 * (min(self.level, 29) + 1)
                    self.score_up += 100 * (min(self.level, 29) + 1)
                    self.for_what_id = 0
                elif cleared == 2:
                    self.score[3] += 300 * (min(self.level, 29) + 1)
                    self.score_up += 300 * (min(self.level, 29) + 1)
                    self.for_what_id = 1
                elif cleared == 3:
                    self.score[4] += 500 * (min(self.level, 29) + 1)
                    self.score_up += 500 * (min(self.level, 29) + 1)
                    self.for_what_id = 2
                elif cleared == 4:
                    self.score[5] += 800 * (min(self.level, 29) + 1)
                    self.score_up += 800 * (min(self.level, 29) + 1)
                    self.for_what_id = 3
                    difficult = True
            if sum(self.cleared_lines) >= self.lines_for_level_up:
                self.level += 1
                self.lines_for_level_up += 10
            if difficult:
                self.back_to_back += 1
                if self.back_to_back > 0:
                    self.score[14] += int((self.score_up*3/2) - self.score_up)
                    self.score_up += int((self.score_up*3/2) - self.score_up)
            else:
                self.back_to_back = -1
            if self.combo > 0:
                self.score[13] += 50 * self.combo * (min(self.level, 29) + 1)
                self.score_up += 50 * self.combo * (min(self.level, 29) + 1)
            self.for_what_delay = 3
        else:
            self.combo = -1
            if t_spin:
                self.score[9] += 400 * (min(self.level, 29) + 1)
                self.score_up = 400 * (min(self.level, 29) + 1)
                self.for_what_id = 7
                self.for_what_delay = 3
            elif t_spin_mini:
                self.score[6] += 100 * (min(self.level, 29) + 1)
                self.score_up = 100 * (min(self.level, 29) + 1)
                self.for_what_id = 4
                self.for_what_delay = 3
        return 0

    def collision(self, next_posx, next_posy, next_id, next_spin_id):
        i1 = next_posy
        k1 = next_posx
        for i in self.TETROMINOS[next_id][next_spin_id]:
            for k in i:
                if k and (i1 >= len(self.FIELD) or k1 >= len(self.FIELD[i1]) or i1 < 0 or k1 < 0 or self.FIELD[i1][k1]):
                    return True
                k1 += 1
            k1 = next_posx
            i1 += 1
        return False

    def spin(self, reverse=False):
        self.reset_lock_delay()
        if self.current_id is not None and self.current_id != 6:
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
                if self.current_id is not None and self.current_id != 5:
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
        if self.current_id is not None and not self.collision(self.current_posx + x_change, self.current_posy, self.current_id, self.current_spin_id):
            self.current_posx += x_change
            self.reset_lock_delay()
            self.spin_is_last_move = False

    def save_state(self):
        i1 = self.current_posy
        k1 = self.current_posx
        if self.current_id is not None:
            for i in self.TETROMINOS[self.current_id][self.current_spin_id]:
                for k in i:
                    if k:
                        self.FIELD[i1][k1] = k
                    k1 += 1
                k1 = self.current_posx
                i1 += 1
        self.pieces[self.current_id] += 1

    def ghost_piece_y(self):
        y = self.current_posy
        while not self.collision(self.current_posx, y + 1, self.current_id,
                                 self.current_spin_id):
            y += 1
        return y

    def reset_lock_delay(self):
        self.lock_delay_frames = 30
        self.lock_delay_run = False

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
                        pygame.draw.rect(win, (int(k.color[0]*self.lock_delay_frames/30), int(k.color[1]*self.lock_delay_frames/30), int(k.color[2]*self.lock_delay_frames/30)), (window_x, window_y, BLOCK_SIZE, BLOCK_SIZE))
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
        if self.for_what_delay > 0.1:
            win.blit(FONT.render(self.for_what_score[self.for_what_id], 1, (230*(min(self.for_what_delay, 1))+25, 230*(min(self.for_what_delay, 1))+25, 230*(min(self.for_what_delay, 1))+25)),
                     (300-int(FONT.size(self.for_what_score[self.for_what_id])[0]/2), 670))
            win.blit(
                FONT.render(f"+{self.score_up}", 1, (230*(min(self.for_what_delay, 1))+25, 230*(min(self.for_what_delay, 1))+25, 230*(min(self.for_what_delay, 1))+25)),
                (300-int(FONT.size(f"+{self.score_up}")[0]/2), 695))
            if self.combo > 0:
                win.blit(
                    FONT.render(f"COMBO × {self.combo}", 1, (
                    230 * (min(self.for_what_delay, 1)) + 25, 230 * (min(self.for_what_delay, 1)) + 25,
                    230 * (min(self.for_what_delay, 1)) + 25)),
                    (300-int(FONT.size(f"COMBO × {self.combo}")[0]/2), 720))
            if self.back_to_back > 0:
                win.blit(
                    FONT.render(f"BACK-TO-BACK × {self.back_to_back}", 1, (
                    230 * (min(self.for_what_delay, 1)) + 25, 230 * (min(self.for_what_delay, 1)) + 25,
                    230 * (min(self.for_what_delay, 1)) + 25)),
                    (300-int(FONT.size(f"BACK-TO-BACK × {self.back_to_back}")[0]/2), 745))
        if self.game_over:
            text_size_x = FONT.size("GAME")[0]
            pygame.draw.rect(win, (0, 0, 0), (223, 327, text_size_x+10, 60))
            pygame.draw.rect(win, (255, 0, 0), (223, 327, text_size_x + 10, 60), width=2)
            win.blit(FONT.render("GAME", 1, (255, 255, 255)), (230, 335))
            win.blit(FONT.render("OVER", 1, (255, 255, 255)), (230, 360))
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


class NesLikeTetris(TetrisGameplay):
    def __init__(self, level=0):
        super().__init__(level, 2, False, False, False, False, False, False, (267, 100), True, 1)

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
        if self.for_what_delay > 0.1:
            win.blit(FONT.render(self.for_what_score[self.for_what_id], 1, (
            230 * (min(self.for_what_delay, 1)) + 25, 230 * (min(self.for_what_delay, 1)) + 25,
            230 * (min(self.for_what_delay, 1)) + 25)),
                     (120, 670))
            win.blit(
                FONT.render(f"+{self.score_up}", 1, (
                230 * (min(self.for_what_delay, 1)) + 25, 230 * (min(self.for_what_delay, 1)) + 25,
                230 * (min(self.for_what_delay, 1)) + 25)),
                (120, 695))
        if self.game_over:
            text_size_x = FONT.size("GAME")[0]
            pygame.draw.rect(win, (0, 0, 0), (223, 327, text_size_x + 10, 60))
            pygame.draw.rect(win, (255, 0, 0), (223, 327, text_size_x + 10, 60), width=2)
            win.blit(FONT.render("GAME", 1, (255, 255, 255)), (230, 335))
            win.blit(FONT.render("OVER", 1, (255, 255, 255)), (230, 360))
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
        win.blit(SMALL_FONT.render(f"QUAD {tetris_times:7d} {self.cleared_lines[3]:5d}      I {self.pieces[5]:<10d}", 1, (255, 255, 255)),
                 (25, 355))
        win.blit(SMALL_FONT.render(f"SCORE TABLE", 1, (255, 255, 255)), (25, 380))
        win.blit(SMALL_FONT.render(f"DROPS {self.score[0]:7d}", 1, (255, 255, 255)), (25, 400))
        win.blit(SMALL_FONT.render(f"SINGLE {self.score[2]:6d}", 1, (255, 255, 255)), (25, 415))
        win.blit(SMALL_FONT.render(f"DOUBLE {self.score[3]:6d}", 1, (255, 255, 255)), (25, 430))
        win.blit(SMALL_FONT.render(f"TRIPLE {self.score[4]:6d}", 1, (255, 255, 255)), (25, 445))
        win.blit(SMALL_FONT.render(f"QUAD {self.score[5]:8d}", 1, (255, 255, 255)), (25, 460))
        pygame.display.update()


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
    g = 0
    delay_before_spawn = -1
    menu_select = 0
    on_pause = False
    corrupted_keys = []
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
            for i in pressed_keys:
                if i in corrupted_keys:
                    pressed_keys.remove(i)
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
            delay_before_spawn = -1
            if selected_gl == 0:
                field = TetrisGameplay(selected_level)
            elif selected_gl == 1:
                field = NesLikeTetris(selected_level)
            pygame.key.set_repeat(field.handling[0], field.handling[1])
            state = "gameplay"
        elif state == "gameplay":
            field.draw_game()
            if not field.game_over:
                if pygame.K_r in pressed_keys:
                    state = "pregameplay"
                if pygame.K_p in pressed_keys:
                    on_pause = True
                    state = "gameplay_stats"
                if pygame.K_UP in pressed_keys or pygame.K_x in pressed_keys:
                    field.spin()
                    corrupted_keys.append(pygame.K_UP)
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
                if pygame.K_LEFT in pressed_keys:
                    field.move_side(-1)
                if pygame.K_RIGHT in pressed_keys:
                    field.move_side(1)
                if pygame.K_SPACE in pressed_keys and field.can_hard_drop:
                    field.move_down(True)
                    field.save_state()
                    field.clear_lines()
                    field.spawn_tetromino()
                    field.lock_delay_run = False
                    field.lock_delay_frames = 30
                    corrupted_keys.append(pygame.K_SPACE)
                field.game_time += clock.get_time()/1000
            if field.for_what_delay > 0:
                field.for_what_delay -= clock.get_time()/1000
            if field.game_over:
                ticks_before_stats -= 1
            if not field.game_over:
                g += field.gravity_and_lines_table()[0]
                if field.soft_drop:
                    g += field.soft_drop_speed
                if g > 22:
                    g = 22
                while g >= 1:
                    if field.support_lock_delay:
                        if not field.move_down():
                            field.lock_delay_run = True
                    else:
                        if not field.move_down():
                            if delay_before_spawn == -1:
                                field.save_state()
                                delay_before_spawn = field.clear_lines()
                                field.current_id = None
                    g -= 1
                if field.nes_mechanics:
                    if delay_before_spawn > -1:
                        delay_before_spawn -= 1
                    if delay_before_spawn == 0:
                        field.spawn_tetromino()
            if field.lock_delay_run:
                field.lock_delay_frames -= 1
                if field.lock_delay_frames <= 0 or not field.support_lock_delay:
                    field.save_state()
                    field.clear_lines()
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
            if pygame.K_p in pressed_keys and not field.game_over:
                on_pause = False
                state = "gameplay"


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
