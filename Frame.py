import wx
from InputPanel import InputPanel
from AllPrimerFinder import AllPrimerFinder
from TargetPrimerFinder import TargetPrimerFinder


class Frame(wx.Frame):
    """ The frame contains the panels which show the input settings and
    result dialogs. It is the main class which handles all the events
    of both dialogs. The most code found in this class is related to
    the input dialog, since those spinners and the text field need to
    be handled properly. More importantly, the values of those settings
    must be shared because the 'xxxx.py' file needs those to actually
    find proper primers. After that, the results must be shown on the
    result screen.
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
        self.input_panel.Bind(wx.EVT_BUTTON, self.handle_primer_button)
        self.Centre()
        self.Show(True)

    def handle_primer_button(self, event):
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
        primers = finder.find_primers()
        # TODO output screen


if __name__ == '__main__':
    # Start the app regularly
    app = wx.App()
    Frame(None, -1, "Simple primer designer")
    app.MainLoop()
