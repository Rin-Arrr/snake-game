import pygame
import random
import sys

# --- Initialisierung von Pygame ---
pygame.init()

# --- Konstanten und Einstellungen ---
# Fenstergröße
FENSTER_BREITE = 800
FENSTER_HOEHE = 600

# Farben (RGB)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (213, 50, 80)
GRUEN = (0, 255, 0)

# Spiel-Einstellungen
BLOCK_GROESSE = 20  # Größe eines Snake-Segments und des Futters
GESCHWINDIGKEIT = 15  # Wie schnell sich die Schlange bewegt (Bilder pro Sekunde)

# --- Fenster und Uhr erstellen ---
fenster = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))
pygame.display.set_caption('Einfaches Snake-Spiel')
clock = pygame.time.Clock()

# Schriftart für den Punktestand und Nachrichten
schrift_stil = pygame.font.SysFont("bahnschrift", 25)
game_over_schrift = pygame.font.SysFont("comicsansms", 50)


# --- Hilfsfunktionen ---

def zeige_punktzahl(punktzahl):
    """Zeigt die aktuelle Punktzahl oben links an."""
    wert = schrift_stil.render("Punkte: " + str(punktzahl), True, WEISS)
    fenster.blit(wert, [10, 10])


def zeichne_snake(snake_block_groesse, snake_liste):
    """Zeichnet alle Segmente der Schlange."""
    for x in snake_liste:
        pygame.draw.rect(fenster, GRUEN, [x[0], x[1], snake_block_groesse, snake_block_groesse])


def nachricht_anzeigen(msg, farbe, y_verschiebung=0):
    """Zeigt eine Nachricht in der Mitte des Bildschirms an."""
    mesg = game_over_schrift.render(msg, True, farbe)
    # Zentriert den Text
    text_rect = mesg.get_rect(center=(FENSTER_BREITE / 2, FENSTER_HOEHE / 2 + y_verschiebung))
    fenster.blit(mesg, text_rect)


# --- Haupt-Spielschleife ---

def spiel_loop():
    spiel_ende = False
    game_over = False

    # Startposition der Schlange (in der Mitte des Fensters)
    x1 = FENSTER_BREITE / 2
    y1 = FENSTER_HOEHE / 2

    # Veränderung der Position (am Anfang bewegt sich die Schlange nicht)
    x1_aenderung = 0
    y1_aenderung = 0

    # Die Schlange ist eine Liste von Koordinaten-Paaren [x, y]
    snake_liste = []
    snake_laenge = 1

    # Position des ersten Futters zufällig generieren
    # Wir runden auf die nächste BLOCK_GROESSE, damit es im Raster bleibt
    futter_x = round(random.randrange(0, FENSTER_BREITE - BLOCK_GROESSE) / BLOCK_GROESSE) * BLOCK_GROESSE
    futter_y = round(random.randrange(0, FENSTER_HOEHE - BLOCK_GROESSE) / BLOCK_GROESSE) * BLOCK_GROESSE

    punktzahl = 0

    # Die eigentliche Spielschleife
    while not spiel_ende:

        # Game-Over-Schleife: Wartet auf die Eingabe des Spielers
        while game_over:
            fenster.fill(SCHWARZ)
            nachricht_anzeigen("Verloren!", ROT, -50)
            nachricht_anzeigen("C: Nochmal spielen | Q: Beenden", WEISS, 50)
            zeige_punktzahl(punktzahl)
            pygame.display.update()

            # Überprüft, ob der Spieler eine Taste drückt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    spiel_ende = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q für Quit (Beenden)
                        spiel_ende = True
                        game_over = False
                    if event.key == pygame.K_c:  # C für Continue (Weiterspielen)
                        spiel_loop()  # Startet das Spiel neu

        # Hauptereignis-Schleife (während das Spiel läuft)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spiel_ende = True
            # Steuerung mit den Pfeiltasten
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_aenderung == 0:
                    x1_aenderung = -BLOCK_GROESSE
                    y1_aenderung = 0
                elif event.key == pygame.K_RIGHT and x1_aenderung == 0:
                    x1_aenderung = BLOCK_GROESSE
                    y1_aenderung = 0
                elif event.key == pygame.K_UP and y1_aenderung == 0:
                    y1_aenderung = -BLOCK_GROESSE
                    x1_aenderung = 0
                elif event.key == pygame.K_DOWN and y1_aenderung == 0:
                    y1_aenderung = BLOCK_GROESSE
                    x1_aenderung = 0

        # Überprüfen, ob die Schlange den Rand berührt -> Game Over
        if x1 >= FENSTER_BREITE or x1 < 0 or y1 >= FENSTER_HOEHE or y1 < 0:
            game_over = True

        # Position der Schlange aktualisieren
        x1 += x1_aenderung
        y1 += y1_aenderung

        # Hintergrund zeichnen
        fenster.fill(SCHWARZ)

        # Futter zeichnen
        pygame.draw.rect(fenster, ROT, [futter_x, futter_y, BLOCK_GROESSE, BLOCK_GROESSE])

        # Schlange aktualisieren und zeichnen
        snake_kopf = [x1, y1]
        snake_liste.append(snake_kopf)

        # Wenn die Schlange zu lang ist, wird das letzte Segment entfernt
        if len(snake_liste) > snake_laenge:
            del snake_liste[0]

        # Überprüfen, ob die Schlange sich selbst berührt -> Game Over
        # Wir prüfen alle Segmente außer dem Kopf
        for segment in snake_liste[:-1]:
            if segment == snake_kopf:
                game_over = True

        zeichne_snake(BLOCK_GROESSE, snake_liste)
        zeige_punktzahl(punktzahl)

        # Alles auf dem Bildschirm anzeigen
        pygame.display.update()

        # Überprüfen, ob die Schlange das Futter frisst
        if x1 == futter_x and y1 == futter_y:
            # Neues Futter an einer zufälligen Position erstellen
            futter_x = round(random.randrange(0, FENSTER_BREITE - BLOCK_GROESSE) / BLOCK_GROESSE) * BLOCK_GROESSE
            futter_y = round(random.randrange(0, FENSTER_HOEHE - BLOCK_GROESSE) / BLOCK_GROESSE) * BLOCK_GROESSE
            snake_laenge += 1
            punktzahl += 1

        # Spielgeschwindigkeit festlegen
        clock.tick(GESCHWINDIGKEIT)

    # Pygame beenden und Programm schließen
    pygame.quit()
    sys.exit()


# --- Spiel starten ---
spiel_loop()