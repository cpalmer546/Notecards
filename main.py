import sys
import csv
import pygame as pg

from button import Button
from notecard import NoteCard


def create_note_cards(font):
    note_card_deck = []
    index = 1

    with open("cards.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_card = NoteCard(font, row['FRONT'], row['BACK'], index)
            note_card_deck.append(new_card)
            index += 1
    return note_card_deck


def main(screen):
    """
    Main game loop

    Takes the pygame screen as param
    """
    study_port_surface = pg.Surface((900, 800))
    study_port_surface.fill('grey')

    font = pg.font.SysFont('Arial', 30)

    main_loop = True
    is_pushed = False
    note_cards = create_note_cards(font)
    current_pos_in_note_cards = 0
    buttons = []
    top_left_of_buttons = [0, 500]
    left_button = Button(top_left_of_buttons[0] + 5, top_left_of_buttons[1], 95, 50, font, '<---', True)
    right_button = Button(top_left_of_buttons[0] + 205, top_left_of_buttons[1], 95, 50, font, '--->', True)
    flip_button = Button(top_left_of_buttons[0] + 105, top_left_of_buttons[1], 95, 50, font, 'Flip', True)
    exit_button = Button(10, 740, 200, 50, font, 'Exit', True)

    buttons.append(exit_button)
    buttons.append(left_button)
    buttons.append(right_button)
    buttons.append(flip_button)

    while main_loop:
        screen.fill('black')
        screen.blit(study_port_surface, (305, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if not is_pushed:
                        is_pushed = True
                        current_pos_in_note_cards += 1

                        if len(note_cards) < current_pos_in_note_cards + 1:
                            current_pos_in_note_cards = 0
                elif event.key == pg.K_LEFT:
                    if not is_pushed:
                        is_pushed = True
                        current_pos_in_note_cards -= 1

                        if current_pos_in_note_cards < 0:
                            current_pos_in_note_cards = len(note_cards) - 1

                elif event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_SPACE:
                    if not is_pushed:
                        is_pushed = True
                        note_cards[current_pos_in_note_cards].turn_card_over()

        note_cards[current_pos_in_note_cards].show_card(screen, font)

        if exit_button.process():
            pg.quit()
            sys.exit()

        for button in buttons:
            button.draw(screen)

        if flip_button.process():
            if not is_pushed:
                is_pushed = True
                note_cards[current_pos_in_note_cards].turn_card_over()
        elif right_button.process():
            if not is_pushed:
                is_pushed = True
                current_pos_in_note_cards += 1

                if len(note_cards) < current_pos_in_note_cards + 1:
                    current_pos_in_note_cards = 0
        elif left_button.process():
            if not is_pushed:
                is_pushed = True
                current_pos_in_note_cards -= 1

                if current_pos_in_note_cards < 0:
                    current_pos_in_note_cards = len(note_cards) - 1
        else:
            is_pushed = False

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    """
    Function to run to start the program
    """
    pg.init()

    main_screen = pg.display.set_mode((1200, 800))
    pg.display.set_caption("Note cards")
    clock = pg.time.Clock()
    main(main_screen)
