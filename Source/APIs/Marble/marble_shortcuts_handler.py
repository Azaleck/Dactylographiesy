import wx
import json

from typing import NamedTuple
from wx.lib.agw.shortcuteditor import ShortcutEditor, Shortcut, KEYMAP, ACCELERATORS

SHORTCUT_PATH = ".shortcut.json"
INV_KEYMAP = dict(zip(KEYMAP.values(), KEYMAP.keys()))
INV_ACCEL = dict(zip(ACCELERATORS.values(), ACCELERATORS.keys()))


def pairFromKey(key_name: str) -> (int, int):
    # '+' cassé ? 'Ctrl++' aussi

    split = key_name.split('+')
    modifiers, key_code = split[0:-1], split[-1]

    base = wx.ACCEL_NORMAL

    for mod in modifiers:
        base |= INV_ACCEL[mod]

    if key_code in INV_KEYMAP:
        key_code = INV_KEYMAP[key_code]
    elif len(key_code) == 1:
        key_code = ord(key_code)
    else:
        key_code = wx.WXK_NONE

    return base, key_code


def getTableFromShortcut(node: Shortcut, editor_table: list, accel_table: list):
    if node.children:
        for child in node.children:
            accel_table = getTableFromShortcut(child, editor_table, accel_table)
    elif node.menuItem is None:
        pair_flags_keycode = pairFromKey(node.accelerator)
        accel_table.append((pair_flags_keycode[0], pair_flags_keycode[1], node.accelId))
        if node.HasChanged():
            for i in range(len(editor_table)):
                if editor_table[i][-1] == node.accelId:
                    editor_table[i] = (editor_table[i][0], pair_flags_keycode[0], pair_flags_keycode[1], node.accelId)
    return accel_table


def determineNewShortcuts(node: Shortcut, sc_dict: dict):
    if node.children:
        for child in node.children:
            determineNewShortcuts(child, sc_dict)
    elif node.HasChanged():
        old_key = node.originalAccelerator
        new_key = node.GetAccelerator()
        for original_key, modified_key in sc_dict.items():
            if old_key == modified_key:
                old_key = original_key
                break
        if old_key == new_key:
            sc_dict.pop(old_key, None)
        else:
            sc_dict[old_key] = new_key


class ShortcutBinds(NamedTuple):
    to_bind: callable
    name_in_menu: str = ""
    key: str = ""


class ShortcutsHandler:

    def _setupShortcutsHandler(self):
        # Loading the dictionary of edited shortcuts.
        try:
            with open(SHORTCUT_PATH, "r") as sc_file:
                self.edited_shortcuts = json.load(sc_file)
        except:
            self.edited_shortcuts = {}

    def _getLocalShortcut(self):
        return [
            # ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.SCROLL_LEFT]),
            #               name_in_menu="Faire défiler à gauche",
            #               key="Left"),
            # ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.SCROLL_RIGHT]),
            #               name_in_menu="Faire défiler à droite",
            #               key="Right"),
            # ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.ENTER, Command.VALIDATE]),  # Selon moi il faudrait enlever validate ici MAIS pbm à replay_or_quit
            #               name_in_menu="Entrer dans un menu ou un jeu",
            #               key="Down"),
            ShortcutBinds(to_bind=lambda _: self._api.onQuit(),
                          name_in_menu="Revenir au menu précédent",
                          key="Up"),
            ShortcutBinds(to_bind=lambda _: self._api.onEraseInput(),
                          name_in_menu="Effacer",
                          key="Back")]

    def _getGlobalShortcut(self):
        return [
            #            ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.REPEAT]),
            #                          name_in_menu="Répéter",
            #                          key="Ctrl+R"),
            #            ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.GET_INFO]),
            #                          name_in_menu="Informations contextuelles",
            #                          key="Ctrl+O"),
            #            ShortcutBinds(to_bind=lambda _: self._api.mediator.executeCommand([Command.GET_RULE]),
            #                          name_in_menu="Règles",
            #                          key="Ctrl+H"),
            ShortcutBinds(to_bind=lambda _: self._api.onReadInput(),
                          name_in_menu="Lire l'entrée",
                          key="Ctrl+I"),
            None,
            ShortcutBinds(to_bind=lambda _: self._api.onValidation(),
                          name_in_menu="Valider une action",
                          key="Enter"),
            ShortcutBinds(to_bind=lambda _: self._api._pause(),
                          name_in_menu="Mettre en pause",
                          key="pause"),
            ShortcutBinds(to_bind=lambda _: self._api.onQuit(),
                          name_in_menu="Quitter",
                          key="Esc")
        ]

    def _createAcceleratorTable(self):
        menu_id = 100  # Start from 100 to avoid conflicts.
        self._accel_table_for_editor = []
        entries = []

        for l_sc in self._getLocalShortcut():
            self.Bind(event=wx.EVT_MENU, handler=l_sc.to_bind, id=menu_id)  # Frame method
            pair_flags_keycode = pairFromKey(self.edited_shortcuts.get(l_sc.key, l_sc.key))
            entries.append(wx.AcceleratorEntry(flags=pair_flags_keycode[0],
                                               keyCode=pair_flags_keycode[1],
                                               cmd=menu_id))
            self._accel_table_for_editor.append((l_sc.name_in_menu,
                                                 pair_flags_keycode[0],
                                                 pair_flags_keycode[1],
                                                 menu_id))
            menu_id += 1

        return wx.AcceleratorTable(entries)

    # =============================================================================================
    #         On event - MenuBar
    # =============================================================================================

    def _onChangeShortcut(self, event):

        # Creating the editor.
        shortcut_editor = ShortcutEditor(self)
        shortcut_editor.SetSize(width=500, height=875)

        # Adding shortcuts to the editor.
        shortcut_editor.FromAcceleratorTable(self._accel_table_for_editor)
        shortcut_editor.FromMenuBar(self)

        # If changes are accepted...
        if shortcut_editor.ShowModal() == wx.ID_OK:
            shortcut_editor.ToMenuBar(self)

            new_table = getTableFromShortcut(node=shortcut_editor.GetShortcutManager(),
                                             editor_table=self._accel_table_for_editor,
                                             accel_table=[])
            self._display_text.SetAcceleratorTable(wx.AcceleratorTable(new_table))

            determineNewShortcuts(shortcut_editor.GetShortcutManager(), self.edited_shortcuts)

            try:
                with open(SHORTCUT_PATH, "w") as sc_file:
                    json.dump(self.edited_shortcuts, sc_file)
            except:
                print("Couldn't save shortcuts properly")
                pass
    
        shortcut_editor.Destroy()
