import wx

from Source.APIs.Marble.marble_shortcuts_handler import ShortcutBinds, ShortcutsHandler


class MarbleMenuBarMixin(ShortcutsHandler):

    def _setupMenuBarMixin(self):

        super()._setupShortcutsHandler()

        # Creating the menu bar.
        self._menu_bar = wx.MenuBar()
        
        # Adding the sub menus.
        self._menu_bar.Append(self.actionMenuBar(), "&Actions")
        self._menu_bar.Append(self.optionMenuBar(), "&Options")
        self._menu_bar.Append(self.helpMenuBar(), "&Aide")

        return self._menu_bar

    # =============================================================================================
    #         Sub menus in menu bar
    # =============================================================================================

    def actionMenuBar(self):
        # Creating the sub menu.
        action_menu = wx.Menu()
        # Adding global shortcuts.
        for g_sc in self._getGlobalShortcut():
            if g_sc is not None:
                self._bindMenu(menu=action_menu, in_menu_id=wx.ID_ANY,
                               shortcut=ShortcutBinds(to_bind=g_sc.to_bind,
                                                      name_in_menu=g_sc.name_in_menu,
                                                      key=self.edited_shortcuts.get(g_sc.key, g_sc.key)))
            else:
                # Adding separator for the look.
                action_menu.AppendSeparator()
        return action_menu

    def optionMenuBar(self):
        # Creating the sub menu.
        option_menu = wx.Menu()
        # Adding shortcut management option.
        self._bindMenu(menu=option_menu, in_menu_id=wx.ID_ANY,
                       shortcut=ShortcutBinds(to_bind=self._onChangeShortcut,
                                              name_in_menu="&Changer les raccourcis",
                                              key=self.edited_shortcuts.get("Ctrl-K", "Ctrl-K")))
        # Adding keyboard option.
        self._bindMenu(menu=option_menu, in_menu_id=wx.ID_ANY,
                       shortcut=ShortcutBinds(to_bind=lambda _: self._api.switchKeyboardMode(),
                                              name_in_menu="&Changer le clavier",
                                              key=self.edited_shortcuts.get("Ctrl-B", "Ctrl-B")))
        # Adding separator for the look.
        option_menu.AppendSeparator()
        # Adding closing option.
        self._bindMenu(menu=option_menu, in_menu_id=wx.ID_EXIT,
                       shortcut=ShortcutBinds(to_bind=self._onExit,
                                              name_in_menu="Fermer la fenêtre"))
        return option_menu

    def helpMenuBar(self):
        # Creating the sub menu.
        help_menu = wx.Menu()
        # Adding help option.
        self._bindMenu(menu=help_menu, in_menu_id=wx.ID_ABOUT,
                       shortcut=ShortcutBinds(to_bind=self._aboutUs,
                                              name_in_menu="En savoir plus"))
        return help_menu

    # =============================================================================================
    #         Auxiliary
    # =============================================================================================

    def _bindMenu(self, menu: wx.Menu, in_menu_id: int, shortcut: ShortcutBinds):
        """ Bind shortcut to the specified menu. """
        action = menu.Append(id=in_menu_id,
                             item=f"{shortcut.name_in_menu}\t{shortcut.key}")
        self.Bind(event=wx.EVT_MENU, handler=shortcut.to_bind, source=action)  # Frame method

    # =============================================================================================
    #         On event - MenuBar
    # =============================================================================================

    def _aboutUs(self, event):
        """ Display a pop-up with information. """
        wx.MessageBox(
            message="Pour toute information complémentaire, consultez notre site web https://handiexceller.com",
            caption="Site web",
            style=wx.OK | wx.ICON_INFORMATION
        )

    def _onExit(self, event):
        """ Close the frame, terminating the application. """
        self.Close(True)  # Frame method
