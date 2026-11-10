FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = FRAME_COLUMNS * FRAME_ROWS
ANIMATION_FPS = 12.0
SHEET_WIDTH = 918
SHEET_HEIGHT = 506
DISPLAY_WIDTH = 184
DISPLAY_HEIGHT = 169
FORMATION_OFFSETS = (-280, -140, 0, 140, 280) * 2
FORMATION_ROWS = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1)
ROW_SPACING = 70
FLIGHT_SPEED = 180.0


def advance_reflected_position(position, direction, distance, minimum, maximum):
    span = maximum - minimum
    if span <= 0:
        return minimum, 0

    phase = position - minimum
    if direction < 0:
        phase = 2 * span - phase
    phase = (phase + distance) % (2 * span)

    if phase < span:
        return minimum + phase, 1
    return minimum + 2 * span - phase, -1


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


class BirdFlock:
    def __init__(self, image, canvas_width, canvas_height):
        self.image = image
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x = canvas_width / 2
        self.direction = 1
        extent = max(abs(offset) for offset in FORMATION_OFFSETS)
        half_bird_width = DISPLAY_WIDTH / 2
        self.minimum_x = extent + half_bird_width
        self.maximum_x = canvas_width - extent - half_bird_width
        if self.minimum_x > self.maximum_x:
            self.minimum_x = self.maximum_x = canvas_width / 2

        self.birds = [
            Bird(image, self.x + offset, self._bird_y(row),
                 index * FRAME_COUNT / 10)
            for index, (offset, row) in enumerate(
                zip(FORMATION_OFFSETS, FORMATION_ROWS)
            )
        ]

    def _bird_y(self, row):
        return self.canvas_height - 90 - row * ROW_SPACING

    def update(self, frame_time):
        self.x, self.direction = advance_reflected_position(
            self.x,
            self.direction,
            FLIGHT_SPEED * frame_time,
            self.minimum_x,
            self.maximum_x,
        )
        for bird in self.birds:
            bird.update(frame_time)

    def draw(self):
        for bird, offset, row in zip(
                self.birds, FORMATION_OFFSETS, FORMATION_ROWS):
            bird.draw(
                self.x + offset,
                self._bird_y(row),
                self.direction > 0,
            )
