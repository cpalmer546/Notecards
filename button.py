import pygame as pg


class Button:
    def __init__(self, x, y, w, h, font, button_text='Button', one_press=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.one_press = one_press
        self.already_pressed = False
        self.return_bool = False

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333'
        }

        # pg.Surface is used to represent images
        self.button_surface = pg.Surface((self.w, self.h))
        # pg.Rect stores rectangular coordinates
        self.button_rect = pg.Rect(self.x, self.y, self.w, self.h)
        # draw text on a new surface
        self.button_surf = font.render(button_text, True, (20, 20, 20))

    def draw(self, screen):
        # gets the mouse position
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])

            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])

        self.button_surface.blit(self.button_surf, [self.button_rect.w / 2 - self.button_surf.get_rect().w / 2, self.button_rect.h / 2 - self.button_surf.get_rect().h / 2])
        screen.blit(self.button_surface, self.button_rect)

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed(num_buttons=3)[0]:

                if self.one_press:
                    self.return_bool = True
                elif not self.already_pressed:
                    self.return_bool = False
                    self.already_pressed = True

            else:
                self.return_bool = False
                self.already_pressed = False

        return self.return_bool
