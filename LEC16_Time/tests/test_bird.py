import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import game_framework
from bird import (
    FRAME_COUNT,
    Bird,
    BirdFlock,
    advance_reflected_position,
)


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_composite_draw(self, *args):
        self.draw_calls.append(args)


class BirdAnimationTests(unittest.TestCase):
    def setUp(self):
        self.previous_frame_time = game_framework.frame_time
        self.image = FakeImage()

    def tearDown(self):
        game_framework.frame_time = self.previous_frame_time

    def test_animation_progress_is_independent_of_frame_rate(self):
        fast_frames = Bird(self.image, 0, 0)
        slow_frames = Bird(self.image, 0, 0)

        for _ in range(30):
            fast_frames.update(1 / 30)
        for _ in range(120):
            slow_frames.update(1 / 120)

        self.assertAlmostEqual(
            fast_frames.animation_frame, slow_frames.animation_frame
        )
        self.assertAlmostEqual(fast_frames.animation_frame, 12.0)

    def test_animation_skips_empty_last_sprite_cell(self):
        bird = Bird(self.image, 0, 0, animation_frame=13)

        bird.draw()
        self.assertEqual(self.image.draw_calls[-1][0], 551)
        self.assertEqual(self.image.draw_calls[-1][1], 0)

        bird.update(1 / 12)
        self.assertEqual(FRAME_COUNT, 14)
        self.assertAlmostEqual(bird.animation_frame, 0.0)

    def test_flock_contains_exactly_ten_birds_and_draws_each(self):
        flock = BirdFlock(self.image, 1600, 600)

        self.assertEqual(len(flock.birds), 10)
        flock.draw()
        self.assertEqual(len(self.image.draw_calls), 10)
        self.assertTrue(all(call[5] == '' for call in self.image.draw_calls))

    def test_flock_travels_at_pixels_per_second(self):
        flock = BirdFlock(self.image, 1600, 600)
        game_framework.frame_time = 0.25

        flock.update()

        self.assertAlmostEqual(flock.x, 845.0)
        self.assertAlmostEqual(flock.birds[0].animation_frame, 3.0)

    def test_flock_distance_is_independent_of_frame_rate(self):
        thirty_fps_flock = BirdFlock(self.image, 1600, 600)
        one_twenty_fps_flock = BirdFlock(self.image, 1600, 600)

        for _ in range(30):
            game_framework.frame_time = 1 / 30
            thirty_fps_flock.update()
        for _ in range(120):
            game_framework.frame_time = 1 / 120
            one_twenty_fps_flock.update()

        self.assertAlmostEqual(thirty_fps_flock.x, 980.0)
        self.assertAlmostEqual(one_twenty_fps_flock.x, 980.0)

    def test_birds_face_the_direction_of_flight(self):
        flock = BirdFlock(self.image, 1600, 600)
        flock.direction = -1

        flock.draw()

        self.assertEqual(len(self.image.draw_calls), 10)
        self.assertTrue(all(call[5] == 'h' for call in self.image.draw_calls))

    def test_reflection_handles_single_and_multiple_bounces(self):
        self.assertEqual(
            advance_reflected_position(90, 1, 30, 10, 100), (80, -1)
        )
        self.assertEqual(
            advance_reflected_position(90, 1, 230, 10, 100), (60, -1)
        )


if __name__ == '__main__':
    unittest.main()
