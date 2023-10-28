import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15, 8))
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interactive Plot')

ax.set(xlim=[0, 50], ylim=[0, 50])
ax.set_aspect('auto', adjustable='box')

xdata = [0]
ydata = [0]
line, = ax.plot(xdata, ydata)


def add_point(event):
    if event.inaxes != ax:
        return

    # button 1: 마우스 좌클릭
    if event.button == 1:

        x = event.xdata
        y = event.ydata

        xdata.append(x)
        ydata.append(y)

        line.set_data(xdata, ydata)
        plt.draw()

    # button 3: 마우스 우클릭 시 기존 입력값 삭제
    if event.button == 3:
        xdata.pop()
        ydata.pop()
        line.set_data(xdata, ydata)
        plt.draw()

    # 마우스 중간버튼 클릭 시 종료하기
    if event.button == 2:
        plt.disconnect(cid)
        plt.close()


cid = plt.connect('button_press_event', add_point)
plt.show()
