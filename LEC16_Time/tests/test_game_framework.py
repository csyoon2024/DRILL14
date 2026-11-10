import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import game_framework


class FrameTimeTests(unittest.TestCase):
    def test_run_passes_elapsed_seconds_to_each_update(self):
        frame_times = []
        original_frame_time = game_framework.frame_time

        class Mode:
            def __init__(self):
                self.frames = 0

            def init(self):
                pass

            def handle_events(self):
                self.frames += 1
                if self.frames == 2:
                    game_framework.quit()

            def update(self):
                frame_times.append(game_framework.frame_time)

            def render(self):
                pass

            def finish(self):
                pass

        try:
            with patch.object(
                    game_framework.time,
                    'perf_counter',
                    side_effect=(100.0, 100.1, 100.35)):
                game_framework.run(Mode())
        finally:
            game_framework.frame_time = original_frame_time

        self.assertAlmostEqual(frame_times[0], 0.1)
        self.assertAlmostEqual(frame_times[1], 0.25)


if __name__ == '__main__':
    unittest.main()
