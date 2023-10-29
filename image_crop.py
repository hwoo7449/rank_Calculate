import cv2
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import time
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

img = cv2.imread('test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_c = plt.imshow(img)
ax = plt.gca()
plt.title('마우스 좌클릭으로 구역을 지정하세요!')

hovering_rect = None


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


def set_pos_hovering_rec(pos: list, x, y):
    # Left-Top
    ltx, lty = pos[0]
    # Right-Bottom
    rbx, rby = x, y

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
            plt.title('나머지 한곳도 눌러주세요!')
        elif len(pos) == 1:
            x, y = event.xdata, event.ydata
            pos.append((x, y))
            point.remove()

            lbcp, width, height = set_pos_rec(pos)
            rect = patches.Rectangle(
                lbcp,      # (x, y) coordinates of left-bottom corner point
                width, height,            # width, height
                edgecolor='Red',
                linestyle='solid',
                fill=False,
                facecolor='yellow',
            )
            ax.add_patch(rect)
            plt.title('다시 선택하시려면 마우스 우클릭, 완료하시려면 엔터를 눌러주세요!')

        plt.draw()

    # button 3: 마우스 우클릭
    if event.button == 3:
        plt.title('마우스 좌클릭으로 구역을 지정하세요!')
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
        cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB, dst=cropped_image)
        cv2.imshow("Cropped Image", cropped_image)
        pass


def move_mouse(event):
    global hovering_rect
    if event.inaxes != ax:
        return

    if len(pos) == 1:
        if hovering_rect is not None:
            hovering_rect.remove()
            hovering_rect = None
        x = event.xdata
        y = event.ydata

        lbcp, width, height = set_pos_hovering_rec(pos, x, y)
        hovering_rect = patches.Rectangle(
            lbcp,      # (x, y) coordinates of left-bottom corner point
            width, height,            # width, height
            edgecolor='Black',
            linestyle='solid',
            fill=False,
            facecolor='yellow',
        )
        ax.add_patch(hovering_rect)

        plt.draw()
        time.sleep(0.01)


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
moving_mouse = plt.connect('motion_notify_event', move_mouse)
plt.show()
