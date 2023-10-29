import cv2
import matplotlib.patches as patches
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

img = cv2.imread('test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_c = plt.imshow(img)
ax = plt.gca()
plt.title('마우스 좌클릭으로 구역을 지정하세요!')


pos = []


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
    global rect
    global point
    if event.inaxes != ax:
        return

    # button 1: 마우스 좌클릭
    if event.button == 1:
        if len(pos) == 0:
            x, y = event.xdata, event.ydata
            pos.append((x, y))
            point = plt.scatter(x, y, c='black')
        elif len(pos) == 1:
            x, y = event.xdata, event.ydata
            pos.append((x, y))
            point.remove()

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

        plt.draw()

    # button 3: 마우스 우클릭
    if event.button == 3:
        pos.clear()
        try:
            rect.remove()

        except ValueError:
            pass
        except NameError:
            pass

        plt.draw()


def end(event):
    if event.key == 'enter':
        plt.disconnect(mouse)
        plt.close()
        cropped_image = crop_image(img, pos)
        cv2.imshow("output", cropped_image)
        pass


def crop_image(img, pos: list):
    # Left-Top
    ltx, lty = pos[0]
    # Right-Bottom
    rbx, rby = pos[1]

    startY = int(lty)
    endY = int(rby)

    startX = int(ltx)
    endX = int(rbx)

    return img[startY:endY, startX:endX]


mouse = plt.connect('button_press_event', add_point)
keyboard = plt.connect('key_press_event', end)
plt.show()
