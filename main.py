import os, sys
import numpy as np
from PIL import Image
from PIL import ImageDraw
from bezier import *

# Отрисовка траектории
draw_debug = True

# Итоговые размеры
W,H = size = (256, 512)

# Загуржаем изображение
src=Image.open("test.jpg").convert("RGBA")
w,h = src.size

# Генериуруем случайную траекторию, 10 точек (х, y, zoom)
points = np.random.rand(10, 3)
# Интерполируем точки с помощью сплайна
path = evaluate_bezier(points, 100)
x, y = path[:,0]*w,  path[:,1]*h
z = path[:,2]*2+0.5

# Рисуем тестовую траекторию на исохдном изображении
if draw_debug:
  xy = (path[:,0:1]*size[0]).astype(int)
  ctx = ImageDraw.Draw(src)
  ctx.polygon(list(zip(x,y)), outline="red")

# Открываем stdout на бинарную запись
with os.fdopen(sys.stdout.fileno(), "wb", closefd=True) as stdout:

    #пробегаемся по точкам сплайна
    for i in range(len(x)):
      # Применяем к изображению трансформацию      
      img = src.transform(size, Image.AFFINE,
        (1.0/z[i], 0.0     , x[i]-W/2.0/z[i],
         0.0     , 1.0/z[i], y[i]-H/2.0/z[i]), resample=Image.BICUBIC)

      # рисуем центр и зум
      if draw_debug:
        ctx = ImageDraw.Draw(img)
        s = 3.0*z[i]
        ctx.ellipse((W/2-s,H/2-s, W/2+s, H/2+s), outline="blue", width=2)

      # Пишем RAW изображения в stout
      stdout.write(img.tobytes())
      stdout.flush()

      # Дальше изображение должен подхвaтить ffmpeg, примерно так:
      # > python main.py | ffplay -f rawvideo -pixel_format rgba -video_size 256x512 -framerate 30 -i -
      # или
      # > python main.py | ffmpeg -f rawvideo -pixel_format rgba -video_size 256x512 -framerate 30 -i - -y output.mp4
