
roomname = '№ 1'
roomname = list(roomname)
rn = 'in '
for i in roomname:
    if i.isdigit():
        rn = rn + i

print(rn)