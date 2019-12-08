import cmath

SIZE = 256

FILE_NAME = 'fractal.ppm'

ITERATIONS = 30

pixmap = bytearray()

STEP = 1 / SIZE

BORDER_COLOR = int(ITERATIONS / 3)

STEP_COLOR = 1 / BORDER_COLOR


def double_range(start, stop, step):
    ret_list = []
    val = start
    if step > 0:
        while True:
            if val >= stop:
                break
            val += step
            ret_list.append(val)
    else:
        while True:
            if val <= stop:
                break
            val += step
            ret_list.append(val)
    return ret_list


def fill_pixmap():
    list_y = double_range(1.0, -1.0, -STEP)
    list_x = double_range(-2.0, 1.0, STEP)
    for y in list_y:
        for x in list_x:
            color = in_set(x, y)
            pixmap.append(color[0])
            pixmap.append(color[1])
            pixmap.append(color[2])


def color_of_iteration(iter_n):
    iter_n += 1;
    if iter_n <= BORDER_COLOR:
        r = STEP_COLOR * iter_n
        g = 0
        b = 0
    elif iter_n <= BORDER_COLOR * 2:
        r = 1
        g = STEP_COLOR * (iter_n - BORDER_COLOR) % 1
        b = 0
    else:
        r = 1
        g = 1
        b = STEP_COLOR * (iter_n - BORDER_COLOR * 2) % 1
    return [ int(255 * r) , int(255 * g), int(255 * b)]


def in_set(x, y):
    z_0 = 0
    c = complex(x, y)
    for iteration in range(ITERATIONS):
        z = z_0 ** 2 + c
        if abs(z) > 2:
            return color_of_iteration(iteration)
        z_0 = z
    return [0, 0, 0]


def write_to_file():
    f = open(FILE_NAME, "bw")
    f.write(create_header())
    f.write(pixmap)
    f.close()


def create_header():
    a = 'P6\n' + str(SIZE * 3) + ' ' + str(SIZE * 2) + '\n255\n'
    return bytearray(a, 'ascii')


def main():
    fill_pixmap()
    write_to_file()


if __name__ == "__main__":
    main()

