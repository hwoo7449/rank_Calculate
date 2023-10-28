import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2

img = cv2.imread('test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_c = plt.imshow(img)
ax = plt.gca()


pos = []
line, = ax.plot('bo-', color='black')


def set_pos_rec(pos: list):
    # Left-Top
    ltx, lty = pos[0]
    # Right-Bottom
    rbx, rby = pos[1]

    # Left-Bottom
    lbx = ltx
    lby = rby

    width = rbx - ltx
    height = lty - rby

    return (lbx, lby), width, height


def add_point(event):
    if event.inaxes != ax:
        return

    # button 1: 마우스 좌클릭
    if event.button == 1:
        if len(pos) == 0:
            x, y = event.xdata, event.ydata
            pos.append((x, y))
            return
        elif len(pos) == 1:
            x, y = event.xdata, event.ydata
            pos.append((x, y))

            lbcp, width, height = set_pos_rec(pos)
            rect = patches.Rectangle(
                lbcp,      # (x, y) coordinates of left-bottom corner point
                width, height,            # width, height
                edgecolor='Black',
                linestyle='solid',
                fill=False,
                facecolor='yellow',
            )
            ax.add_patch(rect)
        elif len(pos) >= 2:
            rect.remove()

        plt.draw()

    # 마우스 중간버튼 클릭 시 종료하기
    if event.button == 2:
        plt.disconnect(cid)
        plt.close()


cid = plt.connect('button_press_event', add_point)
plt.show()
