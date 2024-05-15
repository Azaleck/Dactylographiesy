import wx


class MarbleDisplayMixin:

    def _setupHistoryMixin(self, main_panel):

        # Creating an invisible label. TODO: broken
        wx.StaticText(parent=main_panel, label="Historique").Hide()

        # Creation of the history text zone.
        self._history_text = wx.TextCtrl(parent=main_panel, style=wx.NO_BORDER | wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH2)

        # Setting the font size.
        new_font = self._history_text.GetFont()
        new_font.SetFractionalPointSize(new_font.GetFractionalPointSize()*2)
        self._history_text.SetFont(new_font)

        # Binding the events.
        self._history_text.Bind(wx.EVT_KEY_DOWN, self._api.onKeyPress)
        self._history_text.Bind(wx.EVT_KEY_UP, self._api.onKeyRelease)

        return self._history_text

    def _setupDisplayMixin(self, main_panel, acc_table):

        # Creating an invisible label. TODO: broken
        hidden_text = wx.StaticText(parent=main_panel, id=-1, style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_MIDDLE)
        hidden_text.SetLabel("affichage")
        hidden_text.Hide()

        # Creating the input text zone.
        self._display_text = wx.TextCtrl(parent=main_panel, style=wx.NO_BORDER | wx.TE_READONLY | wx.TE_CENTER | wx.TE_RICH2)
        self._display_text.AcceptsFocusFromKeyboard = lambda: True  # Because no 'wx.TE_MULTILINE'

        # Binding local shortcuts.
        self._display_text.SetAcceleratorTable(acc_table)

        # Binding the events.
        self._display_text.Bind(wx.EVT_KEY_DOWN, self._api.onKeyPress)
        self._display_text.Bind(wx.EVT_KEY_UP, self._api.onKeyRelease)

        # Setting the font size.
        new_font = self._display_text.GetFont()
        font_size = new_font.GetPixelSize().GetHeight()
        new_font.SetFractionalPointSize(new_font.GetFractionalPointSize()*4)
        self._display_text.SetFont(new_font)

        # Setting the minimal height.
        self._display_text.SetMinSize(wx.Size(width=0, height=6*font_size-10))

        # Giving the focus at launch.
        self._display_text.SetFocus()

        return self._display_text

    def _setupParameterTextMixin(self, main_panel, acc_table):
        # Creating the input text zone.
        self._parameter_text = wx.StaticText(parent=main_panel, label="Taille de police", style=wx.NO_BORDER | wx.TE_READONLY | wx.TE_CENTER | wx.TE_RICH2)
        self._parameter_text.AcceptsFocusFromKeyboard = lambda: False  # Because no 'wx.TE_MULTILINE'

        # Binding local shortcuts.
        self._parameter_text.SetAcceleratorTable(acc_table)

        # Setting the font size.
        new_font = self._parameter_text.GetFont()
        font_size = new_font.GetPixelSize().GetHeight()
        new_font.SetFractionalPointSize(new_font.GetFractionalPointSize()*4)
        self._parameter_text.SetFont(new_font)

        # Setting the minimal height.
        self._parameter_text.SetMinSize(wx.Size(width=0, height=6*font_size-10))

        return self._parameter_text

    def _refreshDisplay(self):
        self._display_text.SetValue(self._api.getCurrentDisplay())
        
    def _refreshHistory(self):
        self._history_text.SetValue(self._api.history_handler.viewHistory())
        self._history_text.write("")
