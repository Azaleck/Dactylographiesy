import wx


class MarbleInputMixin:

    def _setupInputMixin(self, main_panel):

        # Creating an invisible label.
        wx.StaticText(parent=main_panel, label="réponse").Hide()

        # Creating the input text zone.
        self._input_text = wx.TextCtrl(parent=main_panel, style=wx.TE_PROCESS_ENTER)

        # Setting the font size.
        new_font = self._input_text.GetFont()
        font_size = new_font.GetPixelSize().GetHeight()
        new_font.SetFractionalPointSize(new_font.GetFractionalPointSize()*2)
        self._input_text.SetFont(new_font)

        # Setting the minimal height.
        self._input_text.SetMinSize(wx.Size(width=0, height=3*font_size+6))

        # Binding the events.
        self._input_text.Bind(wx.EVT_TEXT, self._api.onTextChanged)
        self._input_text.Bind(wx.EVT_TEXT_ENTER, self._api.onValidation)  # style=wx.TE_PROCESS_ENTER needed in TextCtrl
        
        return self._input_text

    def _setupSliderMixin(self, main_panel, nom_slider):

        # Creating an invisible label.
        wx.StaticText(parent=main_panel, label=nom_slider).Hide()

        # Creating the input text zone.
        self._slider = wx.Slider(main_panel, style=wx.SL_LABELS)

        # Setting the font size.
        new_font = self._slider.GetFont()
        font_size = new_font.GetPixelSize().GetHeight()
        new_font.SetFractionalPointSize(new_font.GetFractionalPointSize()*2)
        self._slider.SetFont(new_font)

        # Setting the minimal height.
        self._slider.SetMinSize(wx.Size(width=0, height=3*font_size+6))

        # Setting the min/max values
        self._slider.SetRange(12, 36)

        # Binding the events.
        # self._slider.Bind(wx.EVT_SCROLL, self._api.onSliderChanged)

        return self._slider

    def _resetInputText(self):
        """
        We use 'ChangeValue("")' instead of 'Clear' because 'Clear' would trigger an event.
        """
        self._api.setCurrentInputText("")
        self._input_text.ChangeValue("")

    def _refreshInputText(self):
        self._input_text.ChangeValue(self._api.getCurrentInputText())
