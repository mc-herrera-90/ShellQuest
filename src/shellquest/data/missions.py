
CATEGORIES = [
    {
        "id": "exploration",
        "title": "Exploración",
        "description": "Aprende a navegar por el sistema de archivos.",
        "icon": "folder",
        "missions": [
            {
                "id": "exploration_01",
                "title": "El origen",
                "description": "Llega hasta /home/player/missions.",
                "start_path": "/",
                "target_path": "/home/player/missions",
                "commands": ["pwd", "ls", "cd"],
                "requires": [],
            },
            {
                "id": "exploration_02",
                "title": "Rutas perdidas",
                "description": "Aprende a utilizar rutas absolutas y relativas.",
                "start_path": "/home/player",
                "target_path": "/home/player/missions",
                "commands": ["pwd", "ls", "cd"],
                "requires": ["exploration_01"],
            },
            {
                "id": "exploration_03",
                "title": "El laberinto",
                "description": "Encuentra un directorio escondido.",
                "start_path": "/",
                "target_path": "/var/log",
                "commands": ["pwd", "ls", "cd"],
                "requires": ["exploration_02"],
            },
        ],
    },
    {
        "id": "terminal",
        "title": "Dominio de la terminal",
        "description": "Aprende a ejecutar comandos Linux.",
        "icon": "terminal",
        "missions": [
            {
                "id": "terminal_01",
                "title": "Reconocimiento",
                "description": "Inspecciona los archivos y directorios.",
                "start_path": "/home/player",
                "target_path": "/home/player",
                "commands": ["pwd", "ls"],
                "requires": [],
            },
        ],
    },
]
