# -*- coding: utf-8 -*-

class Localiz:
    def __init__(self, choice):
        self.choice = choice
        self.lang()

    def lang(self):
        if self.choice == 'ru':
            self.MOVE    =  'Двигаться  - ← ↓ →'
            self.DROP    =  'Падение    - space'
            self.ROTATE  =  'Поворот    - ↑'
            self.PAUSE   =  'Пауза      - p'
            self.QUIT    =  'Выход      - q'

            self.SCORE         =  'Очки: '
            self.LINES         =  'Линии: '
            self.LEVEL         =  'Уровень: '
            self.BEST_SCORE    =  'Рекорд: '
            self.STATS         =  'Статистика - s'
            self.BLOCK_STATS   =  'Статистика блоков: '
            self.CLEARED_LINES =  'Всего линий: '
            self.NAME          =  'Введите свое имя (максимум 6):'
            self.CONFIRM       =  'Нажмите Enter для подтверждения'
            self.QUIT_STATS    =  'q - выход'
            self.GAME_OVER     =  ' Игра окончена '
            self.PLAY_AGAIN    =  ' Enter - играть снова '
            self._PAUSE        =  ' Пауза '

        elif self.choice == 'en':
            self.MOVE    =  'Move    - ← ↓ →'
            self.DROP    =  'Drop    - space'
            self.ROTATE  =  'Rotate  - ↑'
            self.PAUSE   =  'Pause   - p'
            self.QUIT    =  'Quit    - q'

            self.SCORE         =  'Score: '
            self.LINES         =  'Lines: '
            self.LEVEL         =  'Level: '
            self.BEST_SCORE    =  'Best Score: '
            self.STATS         =  'Stats - s'
            self.BLOCK_STATS   =  'Blok stats: '
            self.CLEARED_LINES =  'Cleared lines: '
            self.NAME          =  'Enter your name (maximum 6):'
            self.CONFIRM       =  'Press Enter to confirm'
            self.QUIT_STATS    =  'q - quit'
            self.GAME_OVER     =  ' Game Over '
            self.PLAY_AGAIN    =  ' Enter - play again '
            self._PAUSE        =  ' Pause '

        elif self.choice == 'do':
            self.MOVE    =  'bewegen  - ← ↓ →'
            self.DROP    =  'Drop     - space'
            self.ROTATE  =  'Drehen   - ↑'
            self.PAUSE   =  'Pause    - p'
            self.QUIT    =  'Beende   - q'

            self.SCORE         =  'Punktzahl: '
            self.LINES         =  'Zeilen: '
            self.LEVEL         =  'Ebene: '
            self.BEST_SCORE    =  'Bestes Score: '
            self.STATS         =  'Stats - s'
            self.BLOCK_STATS   =  'Blok Statistiken: '
            self.CLEARED_LINES =  'Gelöschte Line: '
            self.NAME          =  'Geben Sie Ihren Namen (max 6):'
            self.CONFIRM       =  'Drücken Eingabet zu bestätigen'
            self.QUIT_STATS    =  'q - beenden'
            self.GAME_OVER     =  ' Spiel vorbei '
            self.PLAY_AGAIN    =  ' Eingeben - erneut '
            self._PAUSE        =  ' Pause '

        elif self.choice == 'fr':
            self.MOVE    =  'Déplacer  - ← ↓ →'
            self.DROP    =  'Déposer   - space'
            self.ROTATE  =  'Rotation  - ↑'
            self.PAUSE   =  'Pause     - p'
            self.QUIT    =  'Quitter   - q'

            self.SCORE         =  'Score: '
            self.LINES         =  'Lignes: '
            self.LEVEL         =  'Niveau: '
            self.BEST_SCORE    =  'Scores: '
            self.STATS         =  'Statistiques - s'
            self.BLOCK_STATS   =  'Statistiques Blok: '
            self.CLEARED_LINES =  'Lignes effacé: '
            self.NAME          =  'Entrez votre nom (maximum 6):'
            self.CONFIRM       =  'Appuyez Entrée pour confirmer'
            self.QUIT_STATS    =  'q - quitter'
            self.GAME_OVER     =  ' Jeu Terminé'
            self.PLAY_AGAIN    =  ' Entrer - rejouer '
            self._PAUSE        =  ' Pause '

        elif self.choice == 'it':
            self.MOVE    =  'Sposta  - ← ↓ →'
            self.DROP    =  'Drop    - space'
            self.ROTATE  =  'Ruota   - ↑'
            self.PAUSE   =  'Pausa   - p'
            self.QUIT    =  'Uscire  - q'

            self.SCORE         =  'Punteggio: '
            self.LINES         =  'Linee: '
            self.LEVEL         =  'Livello: '
            self.BEST_SCORE    =  'Punteggio: '
            self.STATS         =  'Statistica - s'
            self.BLOCK_STATS   =  'Statistiche Blok: '
            self.CLEARED_LINES =  'Linee cancel: '
            self.NAME          =  'Inserisci il tuo nome (max 6):'
            self.CONFIRM       =  'Premere Invio per confermare'
            self.QUIT_STATS    =  'q - uscire'
            self.GAME_OVER     =  ' Gioco finito '
            self.PLAY_AGAIN    =  ' Enter - gioca nuovo '
            self._PAUSE        =  ' Pausa '
