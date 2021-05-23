def curve(lvl):
    return 1/(0.8-((lvl-1)*0.007))**(lvl-1)*0.016666

for i in range(0, 30):
    print(i, curve(i))