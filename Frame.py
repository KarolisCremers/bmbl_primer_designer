import wx
from InputPanel import InputPanel
from ShowPanel import ShowPanel
from AllPrimerFinder import AllPrimerFinder
from TargetPrimerFinder import TargetPrimerFinder


class Frame(wx.Frame):
    """ The frame contains the panels which show the input settings and
    result dialogs. This is the main class which handles the hiding and
    showing of panels. As a result of this, it handles the buttons of
    the panels which should do this.
    """

    def __init__(self, parent, id, title):
        """ Creates the inputpanel, resultpanel and binds events to
        the widgets of those panels.

        Parameters:
            parent - The parent wx Object for this panel.
            id - The id this panel should have.
            title - The title of this frame to be shown on the border
        Returns:
            -
        """
        super(Frame, self).__init__(parent, id, title, size=(600, 285),
                                    style=(wx.MINIMIZE_BOX | wx.SYSTEM_MENU |
                                           wx.CLOSE_BOX | wx.CAPTION |
                                           wx.CLIP_CHILDREN))
        self.input_panel = InputPanel(self, wx.ID_ANY)
        self.input_panel.primers_button.Bind(wx.EVT_BUTTON,
                                             self.handle_primer_button)
        self.show_panel = 0
        self.wrapper_box = wx.BoxSizer(wx.VERTICAL)
        self.wrapper_box.Add(self.input_panel, 1, wx.EXPAND)
        self.SetSizer(self.wrapper_box)
        self.Centre()
        self.Show(True)

    def handle_return(self, event):
        self.show_panel.Hide()
        self.SetSize((600, 313))
        self.input_panel.Show()
        self.Layout()

    def handle_primer_button(self, event):
        """ Handles the event of the Search primers button. This will
        collect all the arguments required for AllPrimerFinder and
        TargetPrimerFinder and will create the correct object according
        to the use_target checkbox; this checkbox defines whether to
        use the target range or not.
        """
        arguments = [self.input_panel.create_primer_checker()]
        for field in ('dna_field', 'anneal_range_minimum',
                      'anneal_range_maximum', 'max_pcr',
                      'target_range_minimum', 'target_range_maximum'):
            arguments.append(getattr(self.input_panel, field).GetValue())
        if self.input_panel.use_target.GetValue():
            finder = TargetPrimerFinder(*arguments)
        else:
            arguments = arguments[:-2]
            finder = AllPrimerFinder(*arguments)
        self.create_show_panel()
        self.show_panel.set_primer(finder.find_primers())
        self.input_panel.Hide()
        self.SetSize((1118, 313))
        self.show_panel.Show()
        self.Layout()

    def create_show_panel(self):
        if self.show_panel:
            self.wrapper_box.Remove(self.show_panel)
        self.show_panel = ShowPanel(self, wx.ID_ANY)
        self.show_panel.return_button.Bind(wx.EVT_BUTTON, self.handle_return)
        self.wrapper_box.Add(self.show_panel, 1, wx.EXPAND)


if __name__ == '__main__':
    # Start the app regularly
    app = wx.App()
    Frame(None, -1, "Simple primer designer")
    app.MainLoop()
