from pywikibot import Site

class MaccabiPediaCragoDumper:
    def __init__(self):
        self.output_path = ""
        self.maccabipedia = Site()
        self.games = dict()
        self.games_events = dict()

    def dump_games_tables(self):
        self.maccabipedia._simple_request(action="cargoquery", )


if __name__ == "__main__":
    cargo_dumper = MaccabiPediaCragoDumper()

    cargo_dumper.dump_games_tables()
