FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = FRAME_COLUMNS * FRAME_ROWS
ANIMATION_FPS = 12.0
SHEET_WIDTH = 918
SHEET_HEIGHT = 506
DISPLAY_WIDTH = 184
DISPLAY_HEIGHT = 169


class Bird:
    def __init__(self, image, x, y, animation_frame=0.0):
        self.image = image
        self.x = x
        self.y = y
        self.animation_frame = animation_frame % FRAME_COUNT

    def update(self, frame_time):
        self.animation_frame = (
            self.animation_frame + ANIMATION_FPS * frame_time
        ) % FRAME_COUNT

    def draw(self, x=None, y=None, facing_right=True):
        frame = int(self.animation_frame)
        column = frame % FRAME_COLUMNS
        row = frame // FRAME_COLUMNS
        source_left = round(column * SHEET_WIDTH / FRAME_COLUMNS)
        source_right = round((column + 1) * SHEET_WIDTH / FRAME_COLUMNS)
        source_top = round(row * SHEET_HEIGHT / FRAME_ROWS)
        source_bottom = round((row + 1) * SHEET_HEIGHT / FRAME_ROWS)
        flip = '' if facing_right else 'h'

        self.image.clip_composite_draw(
            source_left,
            SHEET_HEIGHT - source_bottom,
            source_right - source_left,
            source_bottom - source_top,
            0,
            flip,
            self.x if x is None else x,
            self.y if y is None else y,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT,
        )
