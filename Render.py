import pygame
from World import World


pygame.init()


pygame.font.init()

# Define the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Your Game Title')

class Render:
    def __init__(self, n, m) -> None:
        self.world = World(n,m)
        self.n = n
        self.m = m
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(self.n) for y in range(self.m)]
        self.image = pygame.image.load('data/images/grass.png').convert()
        self.image.set_colorkey((0, 0, 0))
        for i in self.list_x_y:
            self.rect = self.image.get_rect()
            self.rect.center = i

        
            
            
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': 200,'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        
        self.keyboard_speed = 15
        self.mouse_speed = 0.2

        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
    
    def draw(self):
        self.keyboard_control()
        self.zoom_keyboard_control()
        
        screen.fill((255, 255, 255))
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height)]
            image=pygame.transform.scale(self.image, vect_list)
            screen.blit(image, [(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale])

        for k, v in self.world.world.items():
            for obj in v:
                #screen.blit(obj.image, list(eval(k)))           
                vect_list_obj = [x * self.zoom_scale for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
                image_obj=pygame.transform.scale(obj.image, vect_list_obj)
                screen.blit(image_obj, [(list(eval(k))[0]-self.offset.x)*self.zoom_scale,(list(eval(k))[1]-self.offset.y)*self.zoom_scale])
                obj.current_sprite = 0 if  obj.current_sprite == 3 else obj.current_sprite+1
                obj.image = obj.sprites[obj.current_sprite]
                
        pygame.display.flip()
    
   
    
    
    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            self.zoom_scale += 0.1
        if keys[pygame.K_x]:
            self.zoom_scale -= 0.1
        
        
class GameObject(pygame.sprite.Sprite):
    def __init__(self,id):
        super().__init__()
        self.id=id
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png').convert())
        self.sprites.append(pygame.image.load('data/images/1.png').convert())
        self.sprites.append(pygame.image.load('data/images/2.png').convert())
        self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = list([0, 0])

r = Render(30,30)
object1 = GameObject(1)
object2 = GameObject(2)
object3 = GameObject(3)

listObjects = [object1, object2, object3]

r.world.addOnMap(listObjects)


running = True
font = pygame.font.Font(None, 36)
text = font.render("Press S key to save and continue", True,'black')
save_option_shown = False
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # 按下 'S' 键保存游戏状态
                r.world.save_game()
                save_option_shown = False
            elif event.key == pygame.K_ESCAPE:  # 按下 ESC 键显示保存选项
                save_option_shown = True


    if not save_option_shown:
        # 正常游戏逻辑和渲染
        r.draw()
    
        for i in listObjects:
            r.world.move(i)
    else:
        screen.fill('white')
        screen.blit(text, (200, 300))
        pygame.display.flip()
    
    
    clock.tick(20)
    
pygame.quit()