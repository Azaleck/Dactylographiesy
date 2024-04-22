from superjeu import SuperJeu

from definitions import getPhrase


class Jeu1(SuperJeu):

    def __init__(self, notify_gui: callable):
        super().__init__(notify_gui)
        self._valeurIntro = 0

    def estEntree(self, letter) -> bool:
        return letter == " "

    def textPassed(self):
        letter = self.getCurrentInputText()
        phrase = ""

        match self._valeurIntro:
            case 0:
                if self.estEntree(letter):
                    self._valeurIntro += 3
                else:
                    self._valeurIntro += 1
                phrase = getPhrase("intro_jeu_" + str(self._valeurIntro))

            case 3:
                phrase = getPhrase("intro_jeu_3")
                print(phrase)

            case _:  # code un peu pourri, servant de "leçon"
                phrase = "intro_jeu_"
                if self.estEntree(letter):
                    self._valeurIntro += 1
                    phrase += str(self._valeurIntro)
                else:
                    phrase += str(self._valeurIntro)+"_error"
                phrase = getPhrase(phrase)

        self.setNewDisplay(phrase + f" (Tu as écrit : {letter})")

    def run(self):
        self.setNewDisplay(getPhrase("intro_start"))
