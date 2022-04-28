import typer

from weather.utils import get_message
from weather.web_parser import get_temp


def main(city: str) -> None:
    typer.echo(city)
    status, data = get_temp(city)
    msg = get_message(city, status, data)
    typer.echo(msg)


if __name__ == '__main__':
    typer.run(main)
