BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def bold(text):
    return '{}{}{}'.format(BOLD, text, END)
