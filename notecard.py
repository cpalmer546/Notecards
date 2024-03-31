import pygame as pg


class NoteCard:
    front: str
    back: list

    net_plus_section: int
    index: int

    is_turned: bool = False

    def __init__(self, font, front, back, index):
        self.front = front
        self.back = back
        self.index = index

        self.w = 500
        self.h = 250
        self.note_card_surface = pg.Surface((self.w, self.h))
        self.note_card_rect = pg.Rect(500, 300, self.w, self.h)
        self.note_card_surf = font.render(self.display_card_info(), True, (20, 20, 20))

    def turn_card_over(self):
        self.is_turned = not self.is_turned

    def display_card_info(self):
        if self.is_turned:
            return self.back
        else:
            return self.front

    def show_card(self, screen, font):
        if not self.is_turned:
            self.note_card_surface.fill('white')
            self.note_card_surf = font.render(self.display_card_info(), True, (20, 20, 20))
            self.note_card_surface.blit(self.note_card_surf,
                                        [self.note_card_rect.w / 2 - self.note_card_surf.get_rect().w / 2,
                                         self.note_card_rect.h / 2 - self.note_card_surf.get_rect().h / 2])
            screen.blit(self.note_card_surface, self.note_card_rect)

        else:
            font = pg.font.SysFont('Arial', 22)
            self.note_card_surface.fill('white')
            display_text = self.text_wrap_that_hoe(self.display_card_info())

            down_line = 5

            for line in display_text:
                self.note_card_surf = font.render(line, True, (20, 20, 20))
                self.note_card_surface.blit(self.note_card_surf, [2, down_line])
                screen.blit(self.note_card_surface, self.note_card_rect)
                down_line += 25

    def text_wrap_that_hoe(self, info):
        list_of_lines = []
        text_to_app = ''
        for i in info:
            if i == '\n':
                list_of_lines.append(text_to_app)
                text_to_app = ''
            else:
                text_to_app += i
        list_of_lines.append(text_to_app)
        return list_of_lines
