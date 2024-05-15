import datetime
from enum import IntEnum

from definitions import codeIntToChar
from history import HistoryHandler

dots_key_map = {
    ord('D'): 2,
    ord('F'): 1,
    ord('J'): 8,
    ord('K'): 16,
    ord('L'): 32,
    ord('S'): 4
}


class GUIflag(IntEnum):
    CLEAR_INPUT =         0b00000001
    REFRESH_DISPLAY =     0b00000010
    REFRESH_HISTORY =     0b00000100
    ENABLE_INPUT =        0b00001000
    REFRESH_INPUT =       0b00010000
    GIVE_FOCUS_TO_INPUT = 0b00100000


class Parameters:

    def __init__(self, notify_gui: callable):
        self.history_handler = HistoryHandler()
        """
        _normal_mode is True => keyboard qwerty
        _normal_mode is False => keyboard perkins
        """
        self._normal_mode = True
        self._char_by_char = True
        self._input_enabled = True
        self._input_perkins_dict = {}
        self._current_input_text = ""
        self._notifyGUI = notify_gui
        self._display_output = ""

    # =============================================================================================
    #         Getter / Setter
    # =============================================================================================
    # TODO to remove ?

    def isNormalMode(self) -> bool:
        return self._normal_mode

    def isInputEnabled(self) -> bool:
        return self._input_enabled

    def getCurrentDisplay(self) -> str:
        return self._display_output

    def getCurrentInputText(self) -> str:
        return self._current_input_text

    def setCurrentInputText(self, new_text: str):
        self._current_input_text = new_text
        if new_text:
            self.textPassed()

    # Main method that does our logic when inputting something
    def textPassed(self) -> str:
        pass

    # =============================================================================================
    #         Overridden
    # =============================================================================================

    def toHistory(self, s: str, multy_history: bool, once: str):
        self.history_handler.addToHistory(s, multy_history, once)
        self._notifyGUI(GUIflag.REFRESH_HISTORY)

    def setNewDisplay(self, s: str):
        self._display_output = s
        print(f"[Dis] >> '{self._display_output}'")
        self._notifyGUI(GUIflag.REFRESH_DISPLAY)

    def setCharByCharInput(self, char_by_char: bool):
        self._char_by_char = char_by_char
        self._notifyGUI(GUIflag.CLEAR_INPUT)

    def needInput(self, enable: bool):
        self._input_enabled = enable
        self._notifyGUI(GUIflag.ENABLE_INPUT | GUIflag.CLEAR_INPUT)

    # =============================================================================================
    #         On event - For consistency between the 2 modes
    # =============================================================================================

    def onValidation(self):
        self._notifyGUI(GUIflag.CLEAR_INPUT)

    def onEraseInput(self):
        if self._normal_mode and not self._char_by_char:
            if self._current_input_text:
                self._current_input_text = self._current_input_text[:-1]
                self._notifyGUI(GUIflag.REFRESH_INPUT)
        else:
            self._notifyGUI(GUIflag.CLEAR_INPUT)

    def onQuit(self):
        self._notifyGUI(GUIflag.CLEAR_INPUT)

    # =============================================================================================
    #         Input management
    # =============================================================================================

    def onTextChanged(self, event):
        """
        Event triggered each time the input text zone is modified.
        """
        if not self._char_by_char:
            self.setCurrentInputText(event.GetString())
        else:
            self.setCurrentInputText(event.GetString())
            self._notifyGUI(GUIflag.CLEAR_INPUT)

    # =============================================================================================
    #         On event - For keyboard perkins
    # =============================================================================================

    def switchKeyboardMode(self):
        """ Switch keyboard's mode between perkins and qwerty. """
        print(f"-<[ SWITCHED ]>-")
        self._normal_mode = not self._normal_mode
        self._notifyGUI(GUIflag.ENABLE_INPUT | GUIflag.CLEAR_INPUT | GUIflag.GIVE_FOCUS_TO_INPUT)


    def onKeyPress(self, event):
        """
        Event triggered when a key is pressed.
        If keyboard is used as a perkins, then...
        Save the event in a dictionary.
        """
        flag = dots_key_map.get(event.GetKeyCode(), -1) < 0
        if flag or event.IsAutoRepeat() or self._normal_mode:
            event.Skip()
            return

        # Save in dictionary
        dt_now = datetime.datetime.now(datetime.timezone.utc)
        self._input_perkins_dict.update({event.GetKeyCode(): dt_now.timestamp()})

    def onKeyRelease(self, event):
        """
        Event triggered when a key is released.
        If keyboard is used as a perkins, then...
        Compute the letter's code and send it to the api.
        """
        if self._normal_mode:
            event.Skip()
            return
        if event.GetKeyCode() == 32:  # wx.WXK_SPACE but no import
            self.setCurrentInputText(" ")
            event.Skip()
            return
        if dots_key_map.get(event.GetKeyCode(), -1) < 0:
            event.Skip()
            return

        # Save in dictionary
        dt_now = datetime.datetime.now(datetime.timezone.utc)
        self._input_perkins_dict.update({event.GetKeyCode(): -dt_now.timestamp()})

        # Compute the code
        dots_sum = 0
        for key, value in self._input_perkins_dict.items():
            if value > 0:
                return
            if dt_now.timestamp() + value < 0.2:
                dots_sum += dots_key_map.get(key, 0)

        # Send code and reset dictionary
        self.setCurrentInputText(codeIntToChar(dots_sum))
        self._input_perkins_dict = {}

    def run(self):
        self.setNewDisplay("Bienvenue")