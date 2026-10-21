
def execute(command):
    parts = command.strip().split()

    if not parts:
        return ""

    cmd = parts[0]

    if cmd == "help":
        return "Comandos disponibles: help, pwd, ls, cat"

    if cmd == "pwd":
        return "/home/player"

    if cmd == "ls":
        return "Documents  Downloads  pista.txt"

    if cmd == "cat":
        if len(parts) > 1 and parts[1] == "pista.txt":
            return "Pista: encuentra la salida de la habitacion."
        return "Uso: cat pista.txt"

    return f"{cmd}: comando no encontrado"
