class Level:
    def __init__(self, level_name):
        self.level_name = level_name

        self.moveconfig = None
        self.board = None
        self.levelspeed = None
        self.pass_lines = None
        self.pieces_list = {}
        self.piece_speeds = {}
        self.colors_list = {}
        self.sequences_list = {}
        self.scoring = None
        self.startgame_list = []

        self.random_settings = {}
