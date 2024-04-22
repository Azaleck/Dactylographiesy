from superjeu import SuperJeu


class Jeu1(SuperJeu):

    def __init__(self, notify_gui: callable):
        super().__init__(notify_gui)

    def textPassed(self):
        letter = self.getCurrentInputText()
        if letter is "f":
            self.setNewDisplay("bien joué ! maintenant passe d")
        else:
            self.setNewDisplay(f"tu as passé {self._current_input_text} et il fallait passer f")

    def run(self):
        self.setNewDisplay("passe f")
