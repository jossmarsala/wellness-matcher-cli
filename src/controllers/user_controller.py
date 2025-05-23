# Lógica de creación de usuario y formulario

from questionary import text, select, checkbox
from questionary import password as ask_password
from rich import print
from src.utils.app_helpers import save_user
from src.utils.file_helpers import read_json
from src.config.settings import USERS_JSON
from src.models.user import UserModel

def create_user() -> list:
    print("\n¡Comencemos a crear tu usuario 🌷!\n")

    while True:
        username = text("Crea un nombre de usuario").ask()

        if username and username.isalnum():
            read_users = read_json(USERS_JSON)

            if any(user["username"] == username.lower() for user in read_users):
                print(
                    "[bold red]El nombre de usuario que intentaste ingresar ya está en uso.")
                continue
            else:
                break

        print("[bold red]Tu nombre de usuario solo puede estar compuesto por letras y números, intentalo de nuevo.")
        continue

    while True:
        pwd = ask_password("Crea una contraseña").ask()

        if pwd and len(pwd) > 7:
            break

        print(
            "[bold red]Tu contraseña debe tener al menos 8 caracteres, intentalo de nuevo.")
        continue

    while True:
        confirm_password = ask_password("Confirma la contraseña").ask()

        if confirm_password == pwd:
            break

        print("[bold red]Las contraseñas no coinciden.")
        continue

    name = text("¿Cuál es tu nombre completo?").ask()

    print("\nResponde las siguientes preguntas para recibir tus recomendaciones personalizadas ✨")

    disability = select(
        "¿Tienes algún tipo de discapacidad que te impida realizar actividad física?",
        choices=[
            "Sí",
            "No"
        ]
    ).ask()

    physical_activity = select(
        "¿Cuál es tu nivel de actividad física actual?",
        choices=[
            "Sedentario (muy poco o nada de ejercicio)",
            "En transición (busco mejorar mi condición física y aumentar mi nivel de actividad)",
            "Moderado (ejercicio ocasional)",
            "Activo (ejercicio regular)"
        ]
    ).ask()

    diet = select(
        "¿Cómo describirías tu dieta?",
        choices=[
            "Omnívora",
            "Vegetariana o vegana"
        ]
    ).ask()

    while True:
        restrictions = checkbox(
            "¿Tienes alguna restricción alimentaria (intolerancias, alergias)?",
            choices=[
                "Ninguna restricción",
                "Intolerancia a la lactosa",
                "Celiaquía (intolerancia al gluten)",
                "Otros"
            ]
        ).ask()

        if not restrictions:
            print("[bold red]Debes seleccionar al menos una opción.")
            continue

        break

    while True:
        wellbeing_goals = checkbox(
            "¿Cuáles son tus metas en cuanto a tu bienestar?",
            choices=[
                "Reducir el estrés",
                "Mejorar el sueño",
                "Mejorar mi calidad de vida",
                "Conectar más con mi lado espiritual"
            ]
        ).ask()

        if not wellbeing_goals:
            print("[bold red]Debes seleccionar al menos una opción.")
            continue

        break

    while True:
        obstacles = checkbox(
            "¿Qué obstáculos enfrentas para mantener una rutina de bienestar?",
            choices=[
                "Falta de tiempo",
                "Cansancio o fatiga",
                "Niveles altos de autoexigencia",
                "Problemas físicos (movilidad reducida)",
                "Las limitaciones propias de mi edad no me permiten hacer todo lo que quisiera"
            ]
        ).ask()
        if not obstacles:
            print("[bold red]Debes seleccionar al menos una opción.")
            continue

        break

    sleep_quality = select(
        "¿Cómo es tu calidad del sueño?",
        choices=[
            "Duermo entre 5 y 7 horas por noche",
            "Duermo más de 7 horas por noche",
            "Duermo menos de 5 horas por noche"
        ]
    ).ask()

    stress_level = select(
        "¿Sientes estrés y/o ansiedad de forma frecuente?",
        choices=[
            "Sí",
            "No"
        ]
    ).ask()

    daily_routine = select(
        "¿Cómo describirías tu rutina diaria?",
        choices=[
            "Tengo mucho tiempo libre y puedo organizar mi día con flexibilidad",
            "Tengo tiempo libre moderado",
            "Soy una persona ocupada con un horario ajustado"
        ]
    ).ask()

    lifestyle = select(
        "¿Cómo definirías tu estilo de vida?",
        choices=[
            "Soy una persona espiritual",
            "Soy entusiasta del fitness y la vida saludable",
            "Soy una persona centrada en el equilibrio personal",
            "Soy una persona enfocada en llevar un estilo de vida ecológico",
            "Soy una persona con una vida laboral intensa"
        ]
    ).ask()

    username = username.lower()
    password = pwd
    data = {
        "name": name.title(),
        "daily_routine": daily_routine,
        "diet": diet,
        "disability": disability,
        "lifestyle": lifestyle,
        "obstacles": obstacles,
        "physical_activity": physical_activity,
        "restrictions": restrictions,
        "sleep_quality": sleep_quality,
        "stress_level": stress_level,
        "wellbeing_goals": wellbeing_goals
    }

    user = UserModel(username, password, data)
    save_user(user.to_dict())

    print(
        f"\n[bold] ¡Hola, {user.data["name"]}! Ya puedes ver tus recomendaciones.")
