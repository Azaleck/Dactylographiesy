import wx

from marble_wx import MarbleFrame

if __name__ == "__main__":

    main_app = wx.App()  # Required BEFORE frame's creation
    main_frame = MarbleFrame()
    main_frame.beforeMainLoop()

    main_app.MainLoop()

    main_frame.afterMainLoop()