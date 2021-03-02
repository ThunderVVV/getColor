import pyautogui
import cv2
import numpy as np


def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v



def getRealtimeMouseCoordinates():
    color_list = []
    try:
        win = "color preview"
        cv2.namedWindow(win)
        preview = np.zeros((400, 400, 3), dtype=np.uint8)
        xOld = 0
        yOld = 0
        while True:
            xNew, yNew = pyautogui.position()
            if xOld != xNew and yOld != yNew:
                xOld = xNew
                yOld = yNew
                screenshot = pyautogui.screenshot()
                color = screenshot.getpixel((xNew, yNew))
                h, s, v = rgb2hsv(color[0], color[1], color[2])
                # print('X:', '{:>4}'.format(xNew), ', Y:', '{:>4}'.format(yNew), ', RGB:',
                #       '({:>3}, {:>3}, {:>3})'.format(color[0], color[1], color[2]),
                #       'HSV:', 
                #       '({:>3}, {:>3}, {:>3})'.format(h, s, v)
                #       )
            preview[:, :, 0] = color[2]
            preview[:, :, 1] = color[1]
            preview[:, :, 2] = color[0]
            cv2.imshow(win, preview)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('r'):   # 按下r记录当前颜色
                color_list.append('RGB: ' + '{:>3}, {:>3}, {:>3}\n'.format(color[0], color[1], color[2]) + 
                    'HSV: ' + '{:>3}, {:>3}, {:>3}\n'.format(h, s, v))
                print('save RGB: ' + '{:>3}, {:>3}, {:>3}\n'.format(color[0], color[1], color[2]) + 
                    'HSV: ' + '{:>3.3f}, {:>3.3f}, {:>3.3f}\n'.format(h, s, v))
            elif key & 0xFF == ord('q'):  # 摁下q退出
                raise KeyboardInterrupt

    except KeyboardInterrupt:
        if len(color_list) > 0:
            with open("target.out", "w") as f:
                f.writelines(color_list)
        cv2.destroyAllWindows()
        print('Exit')


if __name__ == '__main__':
    getRealtimeMouseCoordinates()