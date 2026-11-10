import os

from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

os.chdir(os.path.dirname(os.path.abspath(__file__)))

open_canvas(1600, 600)
# 프레임 횟수가 아니라 실제 경과 시간(Δt)을 기준으로 비행과 날갯짓을 계산합니다.
# 게임 루프는 단조 시계로 프레임 시간을 재고, 편대는 초당 픽셀 속도 × Δt만큼 이동합니다.
# 화면 경계에서 남은 이동 거리까지 반사 계산해, 프레임 속도가 달라도 이동이 일정합니다.
# 각 새의 애니메이션도 초당 프레임 수 × Δt로 진행하고, 그릴 때 정수 프레임을 선택합니다.
# 스프라이트 시트에서 프레임의 행과 열을 찾아 날개 자세를 그리고, 편대 방향에 맞춰 좌우 반전합니다.
# 따라서 FPS가 달라져도 비행 속도와 날갯짓 속도가 시간 기준으로 유지됩니다.
game_framework.run(start_mode)
close_canvas()
