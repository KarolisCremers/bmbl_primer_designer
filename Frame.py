import wx
import re
from InputPanel import InputPanel


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
        super(Frame, self).__init__(parent, id, title, size=(550, 150),
                                    style=(wx.MINIMIZE_BOX | wx.SYSTEM_MENU |
                                           wx.CLOSE_BOX | wx.CAPTION |
                                           wx.CLIP_CHILDREN))
        self.input_panel = InputPanel(self, -1)
        self.usr_target = False
        self.bind_events()
        self.Centre()
        self.Show(True)

    def bind_events(self):
        """ Binds the events to the widgets of the input panel and
        result panel.

        Parameters:
            -
        Returns:
            -
        """
        self.input_panel.dna_field.Bind(wx.EVT_TEXT, self.check_sequence)
        self.input_panel.dna_field.Bind(wx.EVT_TEXT_PASTE, self.paste_fasta)
        self.input_panel.max_target.Bind(wx.EVT_SPIN, self.target_handler)
        self.input_panel.range_minimum.Bind(wx.EVT_SPIN, self.minimum_handler)
        self.input_panel.range_maximum.Bind(wx.EVT_SPIN, self.maximum_handler)

    def check_sequence(self, *args):
        """ Checks the sequence of the input field and removes unkown
        nucleotides. Case does not matter, but those characters are
        allowed: a, t, c, g, n and x.
        This method also adjusts setting limits so the max value of
        spinners are equal to the length of the given sequence.

        Parameters:
            *args - Any arguments can be given, nothing is done with
            those. This is in place to be compatible with event
            arguments which are not used.
        Returns:
            A boolean whether the check was succesful or not.
        """
        sequence = self.input_panel.dna_field.GetValue()
        sequence = re.sub("[^atcgnxATCGNX]", "", sequence)
        self.input_panel.dna_field.ChangeValue(sequence)
        if sequence:
            length_seq = len(sequence)
            self.input_panel.max_target.SetRange(0, length_seq)
            if not self.usr_target:
                self.input_panel.max_target.SetValue(length_seq)
            self.input_panel.range_minimum.SetRange(1, length_seq - 1)
            self.input_panel.range_maximum.SetRange(2, length_seq)
            return True
        else:
            self.input_panel.max_target.SetRange(0, 1)
            self.input_panel.range_minimum.SetRange(0, 1)
            self.input_panel.range_maximum.SetRange(0, 1)
        return False

    def paste_fasta(self, evt):
        """ Manages the pasting of text into the DNA input field. This
        also supports the FASTA format (for a single sequence) by
        checking for a '>' at the beginning of the text and then simply
        removes the first line.

        Parameters:
            evt - The wx paste event object.
        Returns:
            -
        """
        # Get the paste value
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
        text_data_object = wx.TextDataObject()
        if wx.TheClipboard.GetData(text_data_object):
            text = text_data_object.GetText()
            # Remove fasta header
            if text.startswith('>'):
                data = text.split('\n')
                del data[0]
                text = ''.join(data)
            self.input_panel.dna_field.SetValue(text)
        wx.TheClipboard.Close()

    def target_handler(self, evt):
        """ Checks whether the user manually changed the limit, so the
        application should not auto increment again.

        Parameters:
            evt - The wx Spin event
        Returns:
            -
        """
        if not self.usr_target:
            self.usr_target = True

    def minimum_handler(self, evt):
        """ Handles the spin event for the range_minimum widget, and
        makes sure the range_maximum widget is greater than this
        minimum.

        Parameters:
            evt - The wx Spin event
        Returns:
            -
        """
        value = evt.GetEventObject().GetValue()
        if value >= self.input_panel.range_maximum.GetValue():
            self.input_panel.range_maximum.SetValue(value + 1)

    def maximum_handler(self, evt):
        """ Handles the spin event for the range_maximum widget, and
        makes sure the range_minimum widget is lower than this
        minimum.

        Parameters:
            evt - The wx Spin event
        Returns:
            -
        """
        value = evt.GetEventObject().GetValue()
        if value <= self.input_panel.range_minimum.GetValue():
            self.input_panel.range_minimum.SetValue(value - 1)


if __name__ == '__main__':
    # Start the app regularly
    app = wx.App()
    Frame(None, -1, "Simple primer designer")
    app.MainLoop()

