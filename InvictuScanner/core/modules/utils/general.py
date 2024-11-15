import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ascii_art():
    art = """

 ___            _      ____                                  
|_ _|_ ____   _(_) ___/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
 | || '_ \ \ / / |/ __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | || | | \ V /| | (__ ___) | (_| (_| | | | | | | |  __/ |   
|___|_| |_|\_/ |_|\___|____/ \___\__,_|_| |_|_| |_|\___|_|   

"""
    print(art)

def nice_output(output):
    message = []
    def calc_padding(key):
        return len(max([str(x.get(key)) for x in output.values()], key=len)) + 10
    def head_lines(sizes, lefts="+", middles="+", rights="+", fill="-"):
        messagex = lefts
        iter = 0
        for size in sizes:
            messagex += f"{fill * size}{fill}"
            if iter < len(sizes) - 1:
                messagex += middles
            else:
                messagex += rights
            iter += 1
        message.append(messagex)
    paddings = [calc_padding(key) for key in output.get(list(output.keys())[0])]
    titles = list(output.get(list(output.keys())[0]).keys())
    head_lines(paddings, "╭", "┬", "╮", "─")
    title_bar = "".join(f"│ {title.title()}{' ' * (paddings[titles.index(title)] - len(title))}" for title in titles) + "│"
    message.append(title_bar)
    head_lines(paddings, "├", "┼", "┤", "─")
    for port in list(output.keys()):
        x = 0
        line = ""
        for value in list(output.get(port).values()):
            line += f"│ {value}{' ' * (paddings[x] - len(str(value)))}" if x < len(titles) - 1 else f"│ {value}{' ' * (paddings[x] - len(str(value)))}│"
            x += 1
        message.append(line)
    head_lines(paddings, "╰", "┴", "╯", "─")

    print("\n".join(message))