import random

from superjeu import SuperJeu

from definitions import getPhrase


# Leçon pour apprendre les touches autour du F et du J
class Jeu2(SuperJeu):

    def __init__(self, notify_gui: callable):
        super().__init__(notify_gui)
        load = 0

        self._to_ask = {}
        self.one_remaining = {}
        for letter in "gtrdcvkiuhn":
            # add display string
            display = "Appuie sur la lettre "
            # top/bottom (nous commençons par le milieu, puis haut, milieu, bas)
            if load % 3 != 0:
                if (load // 3) % 2 == 0:
                    display += "en haut "
                else:
                    display += "en bas "

            # left/right
            if ((load + 1) // 3) % 2 == 0:
                display += "à droite "
            else:
                display += "à gauche "

            display += "de la lettre "

            if 5 < load:
                display += "J."
            else:
                display += "F."

            self._to_ask[letter] = display
            self.one_remaining[letter] = False
            load += 1

    def textPassed(self):
        if self.one_remaining == {}:
            self._jeValide(True)
            return
        char_input = self.getCurrentInputText()
        phrase = f"Tu as passé la lettre {char_input}. "

        if char_input == self._letter_to_ask:
            phrase += f"C'est la bonne lettre ! "

            # s'il était déjà juste :
            if self.one_remaining.get(char_input):
                # si correct : remove letter from random
                del self.one_remaining[self._letter_to_ask]

                # fin de jeu : toutes les lettres ont été mises deux fois de suite
                if self.one_remaining == {}:
                    self._jeValide(True)
                    return
            else :
                self.one_remaining[self._letter_to_ask] = True
            print(f"{char_input}, {self.one_remaining}")
        else:
            phrase += f"Ce n'est pas la bonne lettre. La lettre demandée était {self._letter_to_ask}. "
            self.one_remaining[self._letter_to_ask] = False
            # Gérer le cas où une autre lettre que l'exercice fait apprendre est utilisée
            if self._to_ask.get(char_input) is not None:
                self.one_remaining[char_input] = False

        # get next random letter
        self._askForLetter(phrase)

    def _askForLetter(self, phrase: str):
        self._letter_to_ask = random.choice(list(self.one_remaining.keys()))
        if self.one_remaining.get(self._letter_to_ask):
            self.setNewDisplay(f"{phrase} Appuie sur la touche {self._letter_to_ask}.")
        else:
            # Trouver la lettre qui se trouve en haut à droite de _
            self.setNewDisplay(phrase + self._to_ask[self._letter_to_ask])

    def _jeValide(self, finir: bool = False):
        if finir:
            self.setNewDisplay("Tu as réussi l'exercice !")
        else:
            # self._toEnd("Bye bye !", score=0)
            pass

    def run(self):
        self._askForLetter("")
