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
    elif level == 11:
        return 5, 100
    elif level == 12:
        return 5, 100
    elif level == 13:
        return 43, 100
    elif level == 14:
        return 43, 100
    elif level == 15:
        return 43, 100
    elif level == 16:
        return 43, 110
    elif level == 17:
        return 43, 120
    elif level == 18:
        return 43, 130
    elif level == 19:
        return 43, 140
    elif level == 20:
        return 43, 150
    elif level == 21:
        return 43, 160
    elif level == 22:
        return 43, 170
    elif level == 23:
        return 43, 180
    elif level == 24:
        return 43, 190
    elif level == 25:
        return 43, 200
    elif level == 26:
        return 43, 200
    elif level == 27:
        return 43, 200
    elif level == 28:
        return 1, 200
    else:
        return 1, 200


print(speed_and_lines_for_levels(9))
print(speed_and_lines_for_levels(10))
print(speed_and_lines_for_levels(11))
print(speed_and_lines_for_levels(12))
print(speed_and_lines_for_levels(13))
