import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.card import Card
from src.game import Game

# =============================
# Pruebas de la clase Card
# =============================

# T01: Verifica que la carta inicia oculta y no emparejada
def test_estado_inicial_de_carta_es_oculta():
    card = Card("apple", "image")
    assert card.revealed is False
    assert card.matched is False

# T02: Revelar carta cambia su estado a visible
def test_revelar_carta_cambia_estado_a_true():
    card = Card("banana", "image")
    card.reveal()
    assert card.revealed is True

# T03: Ocultar carta revierte el estado a no visible
def test_ocultar_carta_revertir_estado_a_false():
    card = Card("cherry", "image")
    card.reveal()
    card.hide()
    assert card.revealed is False

# T04: Emparejar carta cambia su estado a emparejado
def test_emparejar_carta_cambia_estado_a_true():
    card = Card("lemon", "image")
    card.match()
    assert card.matched is True

# T05: No se puede revelar una carta emparejada
def test_no_se_puede_revelar_carta_emparejada():
    card = Card("orange", "image")
    card.match()
    card.reveal()
    assert card.revealed is False  

# T06: No se puede ocultar una carta emparejada
def test_no_se_puede_ocultar_carta_emparejada():
    card = Card("grape", "image")
    card.reveal()
    card.match()
    card.hide()
    assert card.revealed is True

# T07: Cartas con mismo ID hacen match
def test_cartas_con_mismo_id_hacen_match():
    c1 = Card("apple", "img")
    c2 = Card("apple", "img")
    assert c1.is_match(c2) is True

# T08: Cartas con ID diferente no hacen match
def test_cartas_con_id_diferente_no_hacen_match():
    c1 = Card("apple", "img")
    c2 = Card("banana", "img")
    assert c1.is_match(c2) is False

# T09: Cartas emparejadas aún comparan por ID
def test_cartas_emparejadas_siguen_comparando_por_id():
    c1 = Card("apple", "img")
    c2 = Card("apple", "img")
    c1.match()
    c2.match()
    assert c1.is_match(c2) is True

# T10: Una carta debe hacer match consigo misma
def test_carta_se_compara_consigo_misma():
    c1 = Card("apple", "img")
    assert c1.is_match(c1) is True

# Función auxiliar para tablero simulado
def generar_tablero_dummy(nombres):
    pares = nombres * 2
    random.shuffle(pares)
    return [Card(nombre, "img") for nombre in pares]

# =============================
# Pruebas relacionadas al tablero
# =============================

# T11: El tablero contiene dos cartas por cada nombre
def test_tablero_contiene_todos_los_pares():
    nombres = ["manzana", "uva", "limón"]
    tablero = generar_tablero_dummy(nombres)
    ids = [c.name for c in tablero]
    for nombre in nombres:
        assert ids.count(nombre) == 2

# T12: El orden del tablero debe ser aleatorio
def test_orden_del_tablero_es_aleatorio():
    nombres = ["fresa", "pera", "kiwi"]
    tablero1 = [c.name for c in generar_tablero_dummy(nombres)]
    tablero2 = [c.name for c in generar_tablero_dummy(nombres)]
    assert tablero1 != tablero2  

# T13: Seleccionar carta la añade a la lista y la revela
def test_seleccion_de_carta_agrega_a_lista():
    seleccionadas = []
    carta = Card("limón", "img")
    if not carta.revealed and not carta.matched:
        carta.reveal()
        seleccionadas.append(carta)
    assert len(seleccionadas) == 1
    assert seleccionadas[0].revealed is True

# T14: No se debe añadir carta ya emparejada
def test_no_se_agrega_carta_ya_emparejada():
    seleccionadas = []
    carta = Card("uva", "img")
    carta.match()
    if not carta.revealed and not carta.matched:
        carta.reveal()
        seleccionadas.append(carta)
    assert len(seleccionadas) == 0

# =============================
# Pruebas del juego (Game)
# =============================

# T15: Juego inicia con puntaje e intentos en cero
def test_juego_inicia_con_cero_puntaje_e_intentos():
    juego = Game(["uva", "manzana", "limón"])
    assert juego.score == 0
    assert juego.attempts == 0

# T16: Un intento se registra tras dos turnos
def test_intento_incrementa_tras_dos_selecciones():
    juego = Game(["uva", "manzana", "limón"])
    juego.play_turn(0)
    juego.play_turn(1)
    assert juego.attempts == 1

# T17: Puntaje incrementa al hacer match
def test_puntaje_incrementa_si_hay_match():
    juego = Game(["uva"])
    juego.play_turn(0)
    juego.play_turn(1)
    assert juego.score == 1

# T18: Puntaje no cambia si no hay match
def test_puntaje_no_cambia_si_no_hay_match():
    juego = Game(["uva", "limón", "pera"])
    indices_no_match = []
    for i, c1 in enumerate(juego.board.cards):
        for j, c2 in enumerate(juego.board.cards):
            if i != j and not c1.is_match(c2):
                indices_no_match = [i, j]
                break
        if indices_no_match:
            break
    juego.play_turn(indices_no_match[0])
    juego.play_turn(indices_no_match[1])
    assert juego.score == 0

# =============================
# Segundo Sprint – Vidas y reinicio
# =============================

# T19: Vida disminuye si no hay match
def test_lives_decrementa_si_no_hay_match():
    game = Game(["uva", "limón", "pera"]) 
    indices_no_match = []
    for i, c1 in enumerate(game.board.cards):
        for j, c2 in enumerate(game.board.cards):
            if i != j and not c1.is_match(c2):
                indices_no_match = [i, j]
                break
        if indices_no_match:
            break
    game.play_turn(indices_no_match[0])
    game.play_turn(indices_no_match[1])
    assert game.lives == 4

# T20: Vida no disminuye si hay match
def test_lives_no_decrementa_si_hay_match():
    game = Game(["uva"])
    game.play_turn(0)
    game.play_turn(1)
    assert game.lives == 5  # valor inicial

# T21: El juego debe finalizar al quedarse sin vidas
def test_juego_termina_sin_vidas():
    game = Game(["uva", "limón", "manzana"])
    game.lives = 1
    game.play_turn(0)
    game.play_turn(2)
    assert game.lives == 0
    assert game.game_over() is True

# T22: Reiniciar reinicia todos los valores del juego
def test_reiniciar_resetea_estado_del_juego():
    game = Game(["uva"])
    game.play_turn(0)
    game.play_turn(1)
    game.reiniciar()
    assert game.score == 0
    assert game.attempts == 0
    assert game.lives == 5
    assert all(not c.matched for c in game.board.cards)

# T23: Salir al menú detiene la partida
def test_volver_al_menu_detiene_partida():
    game = Game(["uva"])
    game.salir_a_menu()
    assert game.in_game is False

# T24: Activar o desactivar pausa del juego
def test_menu_pausa_se_activa_con_boton_ajustes():
    game = Game(["uva"])
    game.toggle_pause()
    assert game.paused is True
    game.toggle_pause()
    assert game.paused is False

# =============================
# Tercer Sprint – Temporizador, niveles y animación
# =============================

# T25: El juego avanza de nivel tras match exitoso
def test_juego_avanza_al_siguiente_nivel():
    game = Game(["uva"])
    nivel_anterior = game.nivel
    game.play_turn(0)
    game.play_turn(1)
    assert game.nivel == nivel_anterior + 1
    assert all(not c.revealed for c in game.board.cards)

# T26: Se activa confeti al ganar
def test_se_muestra_animacion_confeti_al_ganar():
    game = Game(["uva"])
    game.play_turn(0)
    game.play_turn(1)
    assert game.confetti_activo is True

# T27: El temporizador incrementa al iniciar el juego
def test_temporizador_inicia_con_juego():
    game = Game(["uva"])
    tiempo_inicial = game.tiempo_inicial
    game.tick()
    assert game.tiempo_inicial > tiempo_inicial


# T28: El temporizador se detiene si el juego está pausado
def test_temporizador_se_detiene_en_pausa():
    game = Game(["uva"])
    game.toggle_pause()
    tiempo_paused = game.tiempo_inicial
    game.tick()
    assert game.tiempo_inicial == tiempo_paused

# T29: El tiempo transcurre mientras el juego está en curso
def test_temporizador_aumenta_con_juego_activo():
    game = Game(["uva"])
    tiempo_inicial = game.tiempo_inicial
    game.tick()
    assert game.tiempo_inicial == tiempo_inicial + 1
