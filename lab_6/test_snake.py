import pytest
import pygame
import math
from snake import Snake, Segment, Apple, check_collision, check_limits, respawn_apple


def test_snake_initialization():
    """Basic Snake initialization test"""
    snake = Snake(100, 200)

    assert snake.x == 100
    assert snake.y == 200
    assert snake.direction == 1 # KEY["UP"]
    assert len(snake.stack) == 2 # Head + black box

def test_snake_move_up():
    """Test snake movement upwards"""
    snake = Snake(100, 200)
    snake.direction = 1
    initial_y = snake.stack[0].y

    snake.move()

    assert snake.stack[0].y < initial_y

if __name__ == "__main__":
    pytest.main([__file__, "-v"])