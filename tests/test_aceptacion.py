def test_activar_menu_pausa_desde_boton():
    game = Game(["uva"])
    assert game.paused is False  # Estado inicial
    game.toggle_pause()          # Activar pausa
    assert game.paused is True   # Verificar que se activó
    game.tick()
    tiempo_despues_tick = game.tiempo_restante
    assert game.tiempo_restante == tiempo_despues_tick  # Cronómetro detenido


def test_reiniciar_juego_resetea_estado_completo():
    game = Game(["uva"])
    game.play_turn(0)
    game.play_turn(1)  # hace match
    assert game.score == 1
    assert game.attempts == 1
    assert game.nivel >= 1

    game.reiniciar()  # Reinicio desde menú de pausa
    assert game.score == 0
    assert game.attempts == 0
    assert game.lives == 5
    assert all(not c.matched for c in game.board.cards)
    assert all(not c.revealed for c in game.board.cards)


def test_volver_al_menu_finaliza_partida():
    game = Game(["uva"])
    assert game.in_game is True
    game.salir_a_menu()
    assert game.in_game is False

#Tercer Sprint
def test_juego_avanza_al_siguiente_nivel():
    game = Game(["uva"])
    nivel_anterior = game.nivel
    game.play_turn(0)
    game.play_turn(1)  # match
    assert game.nivel == nivel_anterior + 1
    assert all(not c.revealed for c in game.board.cards)

def test_se_muestra_animacion_confeti_al_ganar():
    game = Game(["uva"])
    game.play_turn(0)
    game.play_turn(1)
    assert game.confetti_activo is True


def test_temporizador_aumenta_con_juego_activo():
    game = Game(["uva"])
    tiempo_inicial = game.tiempo_jugado
    game.tick()
    assert game.tiempo_jugado == tiempo_inicial + 1

def test_temporizador_se_detiene_en_pausa():
    game = Game(["uva"])
    game.toggle_pause()
    tiempo_paused = game.tiempo_jugado
    game.tick()
    assert game.tiempo_jugado == tiempo_paused
