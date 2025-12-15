import pytest
import pygame
from unittest.mock import patch
from snake import Snake, Apple, check_collision, check_limits, respawn_apple


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


def test_check_collision():
    """Test collision detection"""

    class MockPos:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    pos1 = MockPos(0, 0)
    pos2 = MockPos(5, 5)
    pos3 = MockPos(50, 50)

    assert check_collision(pos1, 10, pos2, 10) == True

    assert check_collision(pos1, 10, pos3, 10) == False


@pytest.mark.parametrize("x,y,expected_x,expected_y", [
    (810, 300, 9, 300),  # За правой границей
    (-10, 300, 791, 300),  # За левой границей
    (400, 610, 400, 9),  # За нижней границей
    (400, -10, 400, 591),  # За верхней границей
    (400, 300, 400, 300),  # В пределах экрана
])
def test_check_limits_parametrized(x, y, expected_x, expected_y):
    """Parametrized test for screen boundary checking"""

    class MockEntity:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    entity = MockEntity(x, y)
    check_limits(entity)

    assert entity.x == expected_x
    assert entity.y == expected_y


def test_snake_grow_with_mock():
    """Test snake growth using mocking"""
    snake = Snake(100, 200)
    initial_length = len(snake.stack)

    snake.stack[-1].direction = 1  # UP

    snake.grow()

    assert len(snake.stack) == initial_length + 2


def test_apple_initialization():
    """Test Apple initialization"""
    apple = Apple(150, 250, 1)

    assert apple.x == 150
    assert apple.y == 250
    assert apple.state == 1
    assert apple.color == pygame.color.Color("red")


@patch('snake.random.uniform')
@patch('snake.math.cos')
@patch('snake.math.sin')
def test_respawn_apple_mocked(mock_sin, mock_cos, mock_uniform):
    """Test apple respawn with mocked random functions"""
    mock_uniform.return_value = 0.5
    mock_cos.return_value = 0.5
    mock_sin.return_value = 0.5

    apples = [Apple(100, 100, 0)]  # Яблоко съедено
    respawn_apple(apples, 0, 200, 200)

    # Проверяем, что яблоко было пересоздано
    assert apples[0].state == 1
    # Проверяем, что координаты изменились
    assert apples[0].x != 100 or apples[0].y != 100


@pytest.mark.parametrize("current_dir,new_dir,expected_dir", [
    (1, 2, 1),  # UP -> DOWN (не должно измениться)
    (2, 1, 2),  # DOWN -> UP (не должно измениться)
    (3, 4, 3),  # LEFT -> RIGHT (не должно измениться)
    (4, 3, 4),  # RIGHT -> LEFT (не должно измениться)
    (1, 3, 3),  # UP -> LEFT (должно измениться)
    (2, 4, 4),  # DOWN -> RIGHT (должно измениться)
])
def test_set_direction_parametrized(current_dir, new_dir, expected_dir):
    """Parametrized test for direction setting"""
    snake = Snake(100, 200)
    snake.direction = current_dir
    snake.set_direction(new_dir)

    assert snake.direction == expected_dir


def test_get_head():
    """Test getting snake head"""
    snake = Snake(100, 200)
    head = snake.get_head()

    assert head == snake.stack[0]
    assert head.x == 100
    assert head.y == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])