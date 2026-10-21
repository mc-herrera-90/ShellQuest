# 🐧 ShellQuest

**Aprende Linux jugando.** ShellQuest es un videojuego educativo desarrollado con Python y Pygame en el que los jugadores aprenderán comandos de Linux mediante misiones, desafíos y preguntas de trivia.

## Requisitos

- [Python 3.13](<https://www.python.org/downloads/>)
- [uv](<https://docs.astral.sh/uv/getting-started/installation/>)

## Instalación

### 1\. Clonar el repositorio

```
git clone <URL_DEL_REPOSITORIO>
cd ShellQuest
```

Si ya tienes el proyecto en tu equipo, entra directamente a su directorio.

### 2\. Instalar uv

Si todavía no tienes `uv` instalado, consulta las instrucciones oficiales:

[https://docs.astral.sh/uv/getting-started/installation/](<https://docs.astral.sh/uv/getting-started/installation/>)

### 3\. Configurar Python

Asegúrate de que `pyproject.toml` permita Python 3.13:

```
requires-python = ">=3.13,<3.14"
```

Fija la versión de Python para el proyecto:

```
uv python pin 3.13
```

Si Python 3.13 no está instalado, `uv` puede descargarlo cuando sea necesario.

### 4\. Instalar las dependencias

```
uv sync
```

Si Pygame todavía no está declarado como dependencia, agrégalo con:

```
uv add pygame
```

### 5\. Ejecutar el juego

Desde la raíz del proyecto:

```
uv run python -m shellquest.main
```

## Desarrollo

Para ejecutar comandos dentro del entorno del proyecto, puedes utilizar `uv run`:

```
uv run python --version
uv run python -m shellquest.main
```

Para agregar nuevas dependencias:

```
uv add nombre-del-paquete
```

## Estructura del proyecto

```
ShellQuest/
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── shellquest/
        ├── __init__.py
        └── main.py
```

## Objetivos del juego

- Aprender comandos básicos de Linux.
- Resolver misiones mediante una terminal simulada.
- Superar preguntas de trivia y desafíos interactivos.
- Desbloquear niveles y progresar en dificultad.

## Tecnologías

- Python
- Pygame
- uv

## Estado del proyecto

🚧 En desarrollo.

Importante: reemplaza `<URL_DEL_REPOSITORIO>` por la URL real de tu repositorio si quieres que otras personas puedan clonarlo. Si el proyecto aún no está publicado, puedes eliminar el paso de clonación y seguir desde la instalación de dependencias.