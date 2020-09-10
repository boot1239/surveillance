from argparse import ArgumentParser

from database.app import init_database
from window import Screen


def setup_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-f',
        '--fullscreen',
        help='Sets the window in fullscreen mode',
        action='store_true'
    )
    parser.add_argument(
        '-n',
        '--new_database',
        help='Creates a new random database',
        action='store_true'
    )
    return parser.parse_args()


def main(args):
    init_database(args)
    Screen(args)


if __name__ == '__main__':
    main(setup_parser())
