import wx

from Source.APIs.Marble.marble_input_mixin import MarbleInputMixin
from Source.APIs.Marble.marble_display_mixin import MarbleDisplayMixin
from Source.APIs.Marble.marble_menubar_mixin import MarbleMenuBarMixin
from jeu2 import Jeu2
from superjeu import SuperJeu, GUIflag
from jeu1 import Jeu1

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 450

DARK_BLUE = wx.Colour(red=24, green=111, blue=159)
LESS_DARK_BLUE = wx.Colour(red=64, green=151, blue=199)
GREY_BLUE = wx.Colour(red=238, green=243, blue=245)
GREYED_OUT = wx.Colour(red=240, green=240, blue=240)

RED = wx.Colour(red=240, green=0, blue=0)
DARK_GREY = wx.Colour(red=40, green=40, blue=40)


LOGO_FILE = "logo.ico"
BACKGROUND_FILE = "image"  # "image.png"


class MarbleFrame(wx.Frame, MarbleDisplayMixin, MarbleInputMixin, MarbleMenuBarMixin):

    def __init__(self):
        """ Constructor. """
        super().__init__(parent=None, title="Marble", size=wx.Size(width=WINDOW_WIDTH, height=WINDOW_HEIGHT))

        self._api = Jeu2(notify_gui=self.callToObserver)

        # Loading images
        self.current_background_image = 0
        self.total_background_images = 16
        self.background_bmp = wx.Bitmap(name=f"{BACKGROUND_FILE}{self.current_background_image}.png", type=wx.BITMAP_TYPE_PNG)
        self.background_bmp_size = wx.Rect(self.background_bmp.GetSize())

        # Setting the font style.
        new_font = self.GetFont()
        new_font.MakeBold()
        self.SetFont(new_font)

        # Setting full screen.
        self.Maximize(True)
        self.SetMinSize(wx.Size(width=WINDOW_MIN_WIDTH, height=WINDOW_MIN_HEIGHT))

        # Creating the menu bar.
        self.SetMenuBar(self._setupMenuBarMixin())

        main_panel = wx.Panel(self)
        main_panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda _: self._resizeBackground(main_panel))

        # Creating the history text zone.
        history_text = self._setupHistoryMixin(main_panel)
        history_text.SetBackgroundColour(GREYED_OUT)
        history_text.SetStyle(start=-1, end=-1, style=wx.TextAttr(colText=DARK_GREY))

        # Creating the display text zone.
        display_text = self._setupDisplayMixin(main_panel, self._createAcceleratorTable())
        display_text.SetBackgroundColour(GREYED_OUT)
        display_text.SetStyle(start=-1, end=-1, style=wx.TextAttr(colText=DARK_BLUE))

        # Creating the input text zone.
        input_text = self._setupInputMixin(main_panel)

        # Setting the layout of the window.
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer.AddStretchSpacer(prop=39)
        input_sizer.Add(window=input_text, proportion=169)
        input_sizer.AddStretchSpacer(prop=39)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.AddStretchSpacer(prop=43)
        left_sizer.Add(window=display_text, proportion=0, flag=wx.EXPAND)
        left_sizer.AddStretchSpacer(prop=10)
        left_sizer.Add(sizer=input_sizer, proportion=0, flag=wx.EXPAND)
        left_sizer.AddStretchSpacer(prop=105)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.AddStretchSpacer(prop=13)
        right_sizer.Add(window=history_text, proportion=147, flag=wx.EXPAND | wx.ALL, border=20)
        right_sizer.AddStretchSpacer(prop=15)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.AddStretchSpacer(prop=12)
        main_sizer.Add(sizer=left_sizer, proportion=198, flag=wx.EXPAND)
        main_sizer.AddStretchSpacer(prop=13)
        main_sizer.Add(sizer=right_sizer, proportion=80, flag=wx.EXPAND)
        main_sizer.AddStretchSpacer(prop=8)
        main_panel.SetSizer(main_sizer)

        self._for_background = main_panel

    def callToObserver(self, flag: int):

        if flag & GUIflag.CLEAR_INPUT:
            self._resetInputText()

        if flag & GUIflag.REFRESH_DISPLAY:
            self._refreshDisplay()

        if flag & GUIflag.REFRESH_HISTORY:
            self._refreshHistory()

        if flag & GUIflag.ENABLE_INPUT:
            self._input_text.Enable(self._api.isInputEnabled() and self._api.isNormalMode())

        if flag & GUIflag.REFRESH_INPUT:
            self._refreshInputText()

        if flag & GUIflag.GIVE_FOCUS_TO_INPUT:
            if self._api.isInputEnabled() and self._api.isNormalMode():
                self._input_text.SetFocus()

    # =============================================================================================
    #         Background handling
    # =============================================================================================

    def _resizeBackground(self, panel):
        dc = wx.ClientDC(panel)  # OS dependent ?
        new_bmp = self.background_bmp.GetSubBitmap(self.background_bmp_size)
        wx.Bitmap.Rescale(bmp=new_bmp, sizeNeeded=dc.GetSize())
        dc.DrawBitmap(bitmap=new_bmp, x=0, y=0)

    def _changeBackground(self, panel, delta):
        self.current_background_image = (self.current_background_image + delta) % self.total_background_images
        self.background_bmp = wx.Bitmap(name=f"{BACKGROUND_FILE}{self.current_background_image}.png", type=wx.BITMAP_TYPE_PNG)
        self.background_bmp_size = wx.Rect(self.background_bmp.GetSize())
        self._resizeBackground(panel)

    # =============================================================================================
    #         APIs methods
    # =============================================================================================

    def beforeMainLoop(self):
        self.Show()
        self._api.run()

    def afterMainLoop(self):
        self._api.__del__()
