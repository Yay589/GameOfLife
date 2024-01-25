import pygame
import sys
import math

pygame.init()

# 设置窗口大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Circular Motion")

# 加载图片
image_ball = pygame.image.load('data/images/full.png')
image_ball = pygame.transform.scale(image_ball, (100, 100))
ball_rect = image_ball.get_rect()

# 设置圆的参数
center_x = width // 2
center_y = height // 2
radius = 200
angle = 0
angular_speed = 0.05  # 角速度，控制运动的速度

clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 计算图片的新位置
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    # 更新角度
    angle += angular_speed

    screen.fill((255, 255, 255))  # 设置背景颜色为白色

    # 绘制图片
    screen.blit(image_ball, (x - ball_rect.width // 2, y - ball_rect.height // 2))

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
