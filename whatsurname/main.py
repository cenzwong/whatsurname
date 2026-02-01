import sys
from . import tui, cli

def main():
    # If arguments are provided, use CLI (Fire)
    # Fire handles help flags (-h, --help) so we should pass them to CLI too
    if len(sys.argv) > 1:
        cli.run()
    else:
        tui.run()

if __name__ == "__main__":
    main()
