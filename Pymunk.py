import pymunk
import pygame
import pymunk.pygame_util

pygame.init()

WIDTH, HEIGHT = 1500, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def crear_rampa(space, width, height):
    p1 = (0, height)
    p2 = (width, height)
    p3 = (0, 0)
    p4 = (p2[0] / 2, (p1[1] / 2))

    ramp = [
        pymunk.Segment(space.static_body, p1, p2, 10),
        pymunk.Segment(space.static_body, p4, p3, 10),  
        pymunk.Segment(space.static_body, p2, p4, 10), 
        pymunk.Segment(space.static_body, p3, p1, 10)
    ]
    for line in ramp:
        line.elasticity = 0.2
        line.friction = 0.4
        space.add(line)

    ramp[2].friction = 20
    return ramp

def crear_rectangulo_con_ruedas(space, x, y, width, height, mass=1):
    moment = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, moment)
    body.position = (x, y)

    shape = pymunk.Poly.create_box(body, (width, height))
    shape.elasticity = 0.2
    shape.friction = 0.2
    shape.collision_type = 2
    space.add(body, shape)

    posiciones_ruedas = [(-30, 30), (30, 30)]
    ruedas = []
    for pos in posiciones_ruedas:
        rueda_body = pymunk.Body(2, float('inf'), body_type=pymunk.Body.DYNAMIC)
        rueda_body.position = body.position + pymunk.Vec2d(*pos)
        rueda_shape = pymunk.Circle(rueda_body, radius=10)
        rueda_shape.elasticity = 0.2
        rueda_shape.friction = 0.2
        space.add(rueda_body, rueda_shape)

        pin_joint = pymunk.PinJoint(body, rueda_body, anchor_a=pos, anchor_b=(0, 0))
        space.add(pin_joint)

        ruedas.append(rueda_body)

    return body, shape, ruedas

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def run(window, width, height):
    try:
        run = True
        clock = pygame.time.Clock()
        fps = 60
        dt = 1 / fps

        space = pymunk.Space()
        space.gravity = (0, 981)  

        rect_width, rect_height = 80, 40  
        rect_x, rect_y = 200, 40  
        rect_body, rect_shape, ruedas = crear_rectangulo_con_ruedas(space, rect_x, rect_y, rect_width, rect_height)
        ramp = crear_rampa(space, width, height)

        draw_options = pymunk.pygame_util.DrawOptions(window)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            draw(space, window, draw_options)
            space.step(dt)
            clock.tick(fps)

        pygame.quit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run(window, WIDTH, HEIGHT)