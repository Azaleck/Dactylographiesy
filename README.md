# Guide d'utilisation pour wxPython

Ce guide a pour vocation de condenser les informations connues à propos de la bibliothèque wxPython. [Cliquez ici](https://docs.wxpython.org) pour accéder à la documentation officielle.

## La fenêtre principale : [wx.Frame](https://docs.wxpython.org/wx.Frame.html)

C'est le parent de tout le monde
Hérite de window
On le show à un moment
L'user peut changer sa taille
Il peut avoir des menus (bar)
Feu la status bar :
```
self.CreateStatusBar()
self.SetStatusText(txt)
menu.Append(... helpString=shortcut.status_message)
```


[wx.Menu](https://docs.wxpython.org/wx.Menu.html)



Needed to create the global menu bar of the application.
You can add menus to it to create sub menus or shortcuts.
Each item added to a menu need to be bind to work.
The '&' marks that the following character will be displayed underlined in the menu, and that this letter acts as a keyboard shortcut.
So if you set the focus to the menu, you can press the underlined letter to execute the action. You can use Alt key to gain to focus to the menu.
i.e.:   

    menu = wx.Menu()
    menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")   # Here we add a stock shortcut to the menu.
    self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

    menu.Append(shortcut_id, "shortcut name \t Ctrl+P", "help message")  # Here we add a custom shortcut to the menu.
    self.Bind(wx.EVT_MENU, self.onShortcut, shortcut_id)

    menu.Append(fileMenu, "&File")  # Here we add the menu to the menu bar.

You can also get and set accelerators of a menu item with GetAccel and SetAccel.
And find a menu item by its id with FindItemById.
i.e.:   

    menu_item = self.menu_bar.FindItemById(id)
    item_accel = menu_item.GetAccel()

    self.menu_bar.FindItemById(id).SetAccel(item_accel)










## La zone principale de la fenêtre : [wx.Panel](https://docs.wxpython.org/wx.Panel.html)

We use the wx.Panel to create the main window of the application.
It's possible to bind events to it to catch specific case you want to handle.
You can also attach this panel to another one to create a sub window or to self to create a main window.

i.e.:

    panel = wx.Panel(self, wx.ID_ANY)
    another_panek = wx.Panel(panel, id=5)
    
    panel.Bind(wx.EVT_KEY_DOWN, onKeyPress)
    panel.SetBackgroundColour(wx.Colour(255, 255, 255))  # RGB Method.
    panel.SetBackgroundColour("light grey")  # RGBA Method  # Color name method.

p.s.: If you want to specify a widget or a panel to be the top window, you can use the following method.
i.e.: self.SetTopWindow(panel)

        main_panel.SetSizer(main_sizer)


        # main_panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: self.trucmuche(main_panel, x))

        def trucmuche(self, panel, evt):
                dc = evt.GetDC()
                
                if not dc:
                    dc = wx.ClientDC(panel)
                    rect = panel.GetUpdateRegion().GetBox()
                    dc.SetClippingRect(rect)
                dc.Clear()
                bmp = wx.Bitmap("Logo_Final_HE_PNG - Copie.png")
                dc.DrawBitmap(bmp, 0, 0)

## L'agencement au sein de la fenêtre : [wx.Sizer](https://docs.wxpython.org/wx.Sizer.html)

Un **[Sizer](https://docs.wxpython.org/wx.Sizer.html)** est un objet qui sert à structurer l'apparence de la fenêtre. Il en existe deux types : les **[BoxSizer](https://docs.wxpython.org/wx.BoxSizer.html)** et les **[GridSizer](https://docs.wxpython.org/wx.GridSizer.html)**. Les **[GridSizer](https://docs.wxpython.org/wx.GridSizer.html)** servent à disposer les éléments sur une grille, nous allons les ignorer dans un premier temps et nous concentrer sur les **[BoxSizer](https://docs.wxpython.org/wx.BoxSizer.html)**. Ces derniers servent à organiser les éléments selon une seule dimension, soit horizontalement, soit verticalement. Pour la déterminer, il faut passer un argument au constructeur, au choix : **wx.HORIZONTAL** ou **wx.VERTICAL**.
```
my_sizer = wx.BoxSizer(wx.HORIZONTAL)
```
Il faut ensuite ajouter des éléments au **[Sizer](https://docs.wxpython.org/wx.Sizer.html)** grâce à la méthode **[Add](https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.Add)**. Les éléments peuvent être des *[Panel](#la-zone-principale-de-la-fenêtre--wxpanel)*, des *[TextCtrl](#gestion-du-texte-dans-la-fenêtre--wxtextctrl)* ou d'autres **[Sizer](https://docs.wxpython.org/wx.Sizer.html)**. La méthode **[AddMany](https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.AddMany)** permet d'ajouter plusieurs éléments d'un coup.
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

# This :

my_sizer.Add(window=my_panel)
my_sizer.Add(window=my_text_ctrl)
my_sizer.Add(sizer=my_other_sizer)

# is the same thing as :

my_sizer.AddMany([my_panel, my_text_ctrl, my_other_sizer])
```
L'argument **proportion** permet de définir la taille d'un élément dans le **[Sizer](https://docs.wxpython.org/wx.Sizer.html)**. S'il est fixé à 0, cela signifie que la taille de l'élément restera fixe. En revanche, s'il est fixé à une valeur positive, cela signifie que la taille de l'élément évoluera proportionnellement avec la taille du **[Sizer](https://docs.wxpython.org/wx.Sizer.html)**. Par exemple, ci-dessous, si *my_sizer* grandit de 3 pixels, *my_first_panel* grandira de 1 pixel, *my_second_panel* restera fixe et *my_third_panel* grandira de 2 pixels.
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

my_sizer.Add(my_first_panel, proportion=1)
my_sizer.Add(my_second_panel, proportion=0)
my_sizer.Add(my_third_panel, proportion=2)
```
Afin de d'harmoniser la position des éléments, on peut ajouter des espaces grâce aux méthodes **[AddSpacer](https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.AddSpacer)** et **[AddStretchSpacer](https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.AddStretchSpacer)** qui permettent respectivement d'ajouter un espace de taille fixe et un espace de taille adaptable.
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

my_sizer.AddStretchSpacer(prop=1)
my_sizer.Add(my_first_panel, proportion=0)
my_sizer.AddSpacer(size=50)
my_sizer.Add(my_second_panel, proportion=0)
my_sizer.AddStretchSpacer(prop=2)
```
L'argument **flag** permet d'indiquer plusieurs comportements qu'un élément va pouvoir cumuler.
- **wx.EXPAND** permet à l'élément de remplir l'espace disponible. Par exemple, ci-dessous, *my_panel* va avoir une taille fixe verticalement mais va occuper toute la largeur du **[Sizer](https://docs.wxpython.org/wx.Sizer.html)**.
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

my_sizer.AddStretchSpacer(prop=1)
my_sizer.Add(my_panel, proportion=0, flag=wx.EXPAND)
my_sizer.AddStretchSpacer(prop=1)
```
- **wx.TOP** / **wx.LEFT** / **wx.RIGHT** / **wx.BOTTOM** permettent d'ajouter une bordure respectivement au-dessus / à gauche / à droite / en-dessous d'un élément. C'est l'argument **border** qui permet de fixer l'épaisseur de la bordure.
- **wx.ALL** permet d'ajouter une bordure tout autour de l'élément (remplace le cumul des quatre arguments ci-dessus)
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

my_sizer.Add(my_first_panel, proportion=0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=20)
my_sizer.Add(my_second_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=20)
```
La méthode **[Clear](https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.Clear)** permet de vider le **[Sizer](https://docs.wxpython.org/wx.Sizer.html)** de ses éléments.
```
my_sizer = wx.BoxSizer(wx.VERTICAL)

my_sizer.AddMany([(my_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20),
                  (my_text_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20),
                  (my_other_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)])

my_sizer.Clear()
```

## Gestion du texte dans la fenêtre : [wx.TextCtrl](https://docs.wxpython.org/wx.TextCtrl.html)


https://docs.wxpython.org/wx.TextEntry.html
TextCtrl is needed to get the input from the user.
You can bind events on it to catch specific case you want to handle.
You can also use methods of wx.TextEntry to handle the content, as SetValue and GetValue.
i.e.:   text = wx.TextCtrl(panel, style=wx.NO_BORDER | wx.TE_CENTER, name="display",
                            value="Hello, World!", size=(200, 800), pos=(0, 0), id=wx.ID_ANY)
        text.Bind(wx.EVT_TEXT, self._onTextChanged)
        str = text.GetValue()
        text.SetValue("new text")
p.s.: SetValue will raise a wx.EVT_TEXT, you can use ChangeValue() to avoid it.

It's also possible to custom the font displayed.
i.e.:   font = text.GetFont()
        font = font.Bold()
        text.SetFont(font)
wx.TE_PROCESS_ENTER needed to validate with the Enter key.

TextCtrl is here needed with the parameter wx.TE_READONLY in order to display what's written to the perkins keayboard.
You can bind events on it to catch specific case you want to handle.
You can also use methods of wx.TextEntry to handle the content, as SetValue and GetValue.
i.e.:   text = wx.TextCtrl(panel, style=wx.NO_BORDER | wx.TE_CENTER, name="display",
                            value="Hello, World!", size=(200, 800), pos=(0, 0), id=wx.ID_ANY)
        text.Bind(wx.EVT_TEXT, self._onTextChanged)
        str = text.GetValue()
        text.SetValue("new text")
p.s.: SetValue will raise a wx.EVT_TEXT, you can use ChangeValue() to avoid it.

It's also possible to custom the font displayed.
https://docs.wxpython.org/wx.Font.html
i.e.:   font = text.GetFont()
        font = font.Bold()
        text.SetFont(font)

TODO: Don't fully understand what AcceptsFocusFromKeyboard do.
i.e.:   text.AcceptsFocusFromKeyboard = True


        font = wx.Font(pointSize=10,
                       family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_BOLD,
                       underline=True,
                       faceName="Jamy")

