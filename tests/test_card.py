import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.card import Card
from src.game import Game

# T01
def test_estado_inicial_de_carta_es_oculta():
    card = Card("apple", "image")
    assert card.revealed is False
    assert card.matched is False

# T02
def test_revelar_carta_cambia_estado_a_true():
    card = Card("banana", "image")
    card.reveal()
    assert card.revealed is True

# T03
def test_ocultar_carta_revertir_estado_a_false():
    card = Card("cherry", "image")
    card.reveal()
    card.hide()
    assert card.revealed is False

# T04
def test_emparejar_carta_cambia_estado_a_true():
    card = Card("lemon", "image")
    card.match()
    assert card.matched is True

# T05
def test_no_se_puede_revelar_carta_emparejada():
    card = Card("orange", "image")
    card.match()
    card.reveal()
    assert card.revealed is False  

# ✅ T06 (corregido)
def test_no_se_puede_ocultar_carta_emparejada():
    card = Card("grape", "image")
    card.reveal()
    card.match()
    card.hide()
    assert card.revealed is True

# T07
def test_cartas_con_mismo_id_hacen_match():
    c1 = Card("apple", "img")
    c2 = Card("apple", "img")
    assert c1.is_match(c2) is True

# T08
def test_cartas_con_id_diferente_no_hacen_match():
    c1 = Card("apple", "img")
    c2 = Card("banana", "img")
    assert c1.is_match(c2) is False

# T09
def test_cartas_emparejadas_siguen_comparando_por_id():
    c1 = Card("apple", "img")
    c2 = Card("apple", "img")
    c1.match()
    c2.match()
    assert c1.is_match(c2) is True

# T10
def test_carta_se_compara_consigo_misma():
    c1 = Card("apple", "img")
    assert c1.is_match(c1) is True

# Función auxiliar
def generar_tablero_dummy(nombres):
    pares = nombres * 2
    random.shuffle(pares)
    return [Card(nombre, "img") for nombre in pares]

# T11
def test_tablero_contiene_todos_los_pares():
    nombres = ["manzana", "uva", "limón"]
    tablero = generar_tablero_dummy(nombres)
    ids = [c.name for c in tablero]
    for nombre in nombres:
        assert ids.count(nombre) == 2

# T12
def test_orden_del_tablero_es_aleatorio():
    nombres = ["fresa", "pera", "kiwi"]
    tablero1 = [c.name for c in generar_tablero_dummy(nombres)]
    tablero2 = [c.name for c in generar_tablero_dummy(nombres)]
    assert tablero1 != tablero2  

# T13
def test_seleccion_de_carta_agrega_a_lista():
    seleccionadas = []
    carta = Card("limón", "img")
    if not carta.revealed and not carta.matched:
        carta.reveal()
        seleccionadas.append(carta)
    assert len(seleccionadas) == 1
    assert seleccionadas[0].revealed is True

# T14
def test_no_se_agrega_carta_ya_emparejada():
    seleccionadas = []
    carta = Card("uva", "img")
    carta.match()
    if not carta.revealed and not carta.matched:
        carta.reveal()
        seleccionadas.append(carta)
    assert len(seleccionadas) == 0

# T15
def test_juego_inicia_con_cero_puntaje_e_intentos():
    juego = Game(["uva", "manzana", "limón"])
    assert juego.score == 0
    assert juego.attempts == 0

# T16
def test_intento_incrementa_tras_dos_selecciones():
    juego = Game(["uva", "manzana", "limón"])
    juego.play_turn(0)
    juego.play_turn(1)
    assert juego.attempts == 1

# T17
def test_puntaje_incrementa_si_hay_match():
    juego = Game(["uva"])
    juego.play_turn(0)
    juego.play_turn(1)
    assert juego.score == 1

# T18
def test_puntaje_no_cambia_si_no_hay_match():
    juego = Game(["uva", "limón"])
    juego.play_turn(0)
    juego.play_turn(2)
    assert juego.score == 0

# T19
def test_juego_finaliza_cuando_todas_las_cartas_emparejadas():
    juego = Game(["uva"])
    juego.play_turn(0)
    juego.play_turn(1)
    assert juego.game_over() is True
