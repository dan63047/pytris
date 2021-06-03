def curve(lvl):
    return 1/(0.8-((lvl-1)*0.007))**(lvl-1)*0.016666

def delay_curve(lvl):
    return min(30, 90-3*lvl)

for i in range(0, 31):
    print(i, curve(i), delay_curve(i))