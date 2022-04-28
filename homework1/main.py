import os
import typer

import utils
from player import Player
from autoplayer import AutoPlayer
from static_data import MoveResult, ProcessInputResult, AUTOSAVE_NAME
from text_data import TextData


def main(
    height: int = 10,
    width: int = 10,
    automove: bool = False,
    autoplay: bool = False,
):

    typer.echo(TextData.WELCOME)

    input_ok, msg = utils.check_size_limits(height, width)
    if not input_ok:
        typer.echo(msg)
        return

    typer.echo(TextData.INIT.format(height, width))

    player, enemy_player = None, None
    if os.path.exists(AUTOSAVE_NAME):
        ans = input(TextData.FOUND_AUTOSAVE).lower()
        if ans == "y" or ans == "yes":
            player, enemy_player = utils.load_game()
            if player is None or enemy_player is None:
                typer.echo(TextData.ERROR_LOAD_AUTOSAVE, err=True)

    if player is None and enemy_player is None:
        player = Player(height, width)
        enemy_player = AutoPlayer(height, width)
    elif player is None or enemy_player is None:
        typer.echo(TextData.ERROR_LOAD_AUTOSAVE, err=True)
        player = Player(height, width)
        enemy_player = AutoPlayer(height, width)
    if automove or autoplay:
        player = AutoPlayer(height, width)
    len_of_field = player.get_len_of_field()
    len_of_borders_your = len_of_field - len(TextData.YOUR_FIELD_NAME)
    len_of_borders_opp = len_of_field - len(TextData.OPP_FIELD_NAME)
    len_of_borders_your = (
        len_of_borders_your // 2,
        len_of_borders_your // 2 + len_of_borders_your % 2,
    )
    len_of_borders_opp = (
        len_of_borders_opp // 2,
        len_of_borders_opp // 2 + len_of_borders_opp % 2,
    )

    game_over = False
    last_message = ""
    is_save = False
    enemy_wins = False

    while not game_over and not is_save:
        input_ok = False
        while not input_ok:
            typer.echo(
                " " * len_of_borders_your[0]
                + TextData.YOUR_FIELD_NAME
                + " " * len_of_borders_your[1]
                + "\t"
                + " " * len_of_borders_opp[0]
                + TextData.OPP_FIELD_NAME
                + " " * len_of_borders_opp[1]
            )
            if game_over or enemy_wins:
                player.enemy_field = enemy_player.field
                game_over = True
            player.print_fields()
            if last_message:
                typer.secho(last_message, fg=typer.colors.RED)
                last_message = ""
            if game_over:
                break
            typer.echo(TextData.ENTER_MOVE)
            if automove or autoplay:
                row_index, col_index, move_res = player.make_auto_move(
                    enemy_player
                )
                input_ok = True
                typer.echo(
                    TextData.YOUR_MOVE
                    + utils.move_to_str(row_index, col_index)
                )
                if not autoplay:
                    input()
            else:
                move, row_index, col_index = utils.process_input(
                    input().upper()
                )
                if move == ProcessInputResult.SAVE:
                    utils.save_game(player, enemy_player)
                    is_save = True
                    typer.echo(TextData.GAME_SAVED)
                    break
                if move == ProcessInputResult.WRONG:
                    last_message = TextData.WRONG_MOVE
                    continue
                input_ok, move_res = player.make_move(
                    row_index, col_index, enemy_player
                )
                if not input_ok:
                    last_message = TextData.WRONG_MOVE
                    continue
            if move_res == MoveResult.EMPTY:
                last_message = TextData.EMPTY_MOVE
            elif move_res == MoveResult.HIT:
                last_message = TextData.HIT_MOVE
                input_ok = False
            elif move_res == MoveResult.SINK:
                last_message = TextData.SINK_MOVE
                input_ok = False
            elif move_res == MoveResult.WIN:
                game_over = True
                input_ok = False
                continue
            else:
                print(row_index, col_index, input_ok, move_res)
                raise RuntimeError()
        if not game_over:
            enemy_make_move = True
            while enemy_make_move:
                enemy_make_move = False
                row_index, col_index, move_res = enemy_player.make_auto_move(
                    player
                )
                last_message += TextData.ENEMY_MOVE.format(
                    utils.move_to_str(row_index, col_index), move_res.name
                )
                if move_res == MoveResult.EMPTY:
                    break
                elif move_res == MoveResult.WIN:
                    enemy_wins = True
                    break
                elif move_res == MoveResult.HIT or move_res == MoveResult.SINK:
                    enemy_make_move = True
                else:
                    print(row_index, col_index, input_ok, move_res)
                    raise RuntimeError()
    if enemy_wins:
        typer.secho(TextData.YOU_LOSE, fg=typer.colors.RED)
    else:
        typer.secho(TextData.YOU_WIN, fg=typer.colors.RED)

    if not is_save:
        if os.path.exists(AUTOSAVE_NAME):
            try:
                os.remove(AUTOSAVE_NAME)
            except Exception:
                typer.echo(TextData.ERROR_DELETE_AUTOSAVE, err=True)


if __name__ == "__main__":
    typer.run(main)
