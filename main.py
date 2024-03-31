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
    Main game function

    Takes the pygame screen as param
    """
    study_port_surface = pg.Surface((900, 800))
    study_port_surface.fill('grey')

    font = pg.font.SysFont('Arial', 30)

    # Game variables
    main_loop = True
    is_pushed = False
    note_cards = create_note_cards(font)
    current_pos_in_note_cards = 0
    buttons = []
    top_left_of_buttons = [0, 350]

    # Create buttons
    left_button = Button(top_left_of_buttons[0] + 5, top_left_of_buttons[1], 95, 50, font, '<---', True)
    right_button = Button(top_left_of_buttons[0] + 205, top_left_of_buttons[1], 95, 50, font, '--->', True)
    flip_button = Button(top_left_of_buttons[0] + 105, top_left_of_buttons[1], 95, 50, font, 'Flip', True)

    turn_all_cards_front_upright = Button(top_left_of_buttons[0] + 40, top_left_of_buttons[1] + 110, 220, 50, font,
                                          "Turn cards upright", True)

    turn_all_cards_front_down = Button(top_left_of_buttons[0] + 40, top_left_of_buttons[1] + 165, 220, 50, font,
                                       "Turn cards down", True)

    exit_button = Button(10, 740, 110, 50, font, 'Exit', True)

    # add all buttons to a list to be able to iterate over them
    buttons.append(left_button)
    buttons.append(right_button)
    buttons.append(flip_button)
    buttons.append(turn_all_cards_front_upright)
    buttons.append(turn_all_cards_front_down)
    buttons.append(exit_button)

    # main game loop
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

        # displays the card on screen with .show_card method
        note_cards[current_pos_in_note_cards].show_card(screen, font)

        if exit_button.process():
            pg.quit()
            sys.exit()

        # iterate over button list to show buttons on screen
        for button in buttons:
            button.draw(screen)

        # some checks to see if any of the buttons were pressed
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

        elif turn_all_cards_front_upright.process():
            if not is_pushed:
                is_pushed = True
                for card in note_cards:
                    card.is_turned = False

        elif turn_all_cards_front_down.process():
            if not is_pushed:
                is_pushed = True
                for card in note_cards:
                    card.is_turned = True
        else:
            is_pushed = False

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    """
    The start of code execution
    """
    pg.init()

    main_screen = pg.display.set_mode((1200, 800))
    pg.display.set_caption("Note cards")
    clock = pg.time.Clock()
    main(main_screen)
