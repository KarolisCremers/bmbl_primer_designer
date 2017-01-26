from PrimerChecker import PrimerChecker
import wx
import re


def event_wrapper(func, *args, **kwargs):
    """ Wraps a function so multiple arguments can be given to a method
    which handles an event.

    Parameters:
        func - The method or function which should be executed.
        *args - A form of varargs, any parameter can be given
        **kwargs - A form of named varargs, any parameter can be given
    Returns:
        A lambda function wrapping the function to be executed
    """
    return lambda evt: func(evt, *args, **kwargs)


def default_spinner(parent):
    spin = wx.SpinCtrl(parent, wx.ID_ANY,
                       style=InputPanel.SPINNER_STYLE)
    spin.SetRange(0, 0)
    return spin


class InputPanel(wx.Panel):
    """ This is the panel which contains all the input fields in the
    layout. The behaviour however is not defined in this class, as
    this currently is done by Frame.py. This has to do with the fact
    that the two panels in this application need to communicate with
    each other, and thus the Frame will contain and define behaviour.
    """

    # The default spinner style
    SPINNER_STYLE = (wx.SP_HORIZONTAL | wx.SP_ARROW_KEYS | wx.SP_WRAP)

    def __init__(self, parent, id):
        """ Creates the main Sizer container and calls
        # create_dna_input and #create_settings_box to fill this
        container. Then this containeR is put in another container
        which makes sure there are 5 pixels around the border.

        Parameters:
            parent - The parent wx Object for this panel.
            id - The id this panel should have.
        Returns:
            -
        """
        super(InputPanel, self).__init__(parent, id)
        self.skip_additional = False
        required_input = wx.BoxSizer(wx.HORIZONTAL)
        required_input.Add(self.create_dna_input(), 1, wx.EXPAND)
        required_input.Add(self.create_settings_box(), 1, wx.EXPAND | wx.LEFT,
                           5)
        padding_box = wx.BoxSizer(wx.VERTICAL)
        padding_box.Add(required_input, 1, wx.EXPAND | wx.ALL, 5)
        padding_box.Add(self.create_optional_input(), 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(padding_box)
        self.bind_events()

    def create_primer_checker(self):
        """ Creates a new PrimerChecker object according to the
        experimental checking values in the gui. Those are from the
        widgets dimer_check, self_dimer_check and hairpin_check.

        Parameters:
            -
        Returns:
            A new PrimerChecker object with the correct settings
        """
        check_dimer = self.dimer_check.GetValue()
        check_self_dimer = self.self_dimer_check.GetValue()
        check_hairpin = self.hairpin_check.GetValue()
        return PrimerChecker(dimer=check_dimer, self_dimer=check_self_dimer,
                             hairpin=check_hairpin)

    ## Event methods

    def bind_events(self):
        """ Binds the events to the widgets of this and
        result panel.
        """
        self.dna_field.Bind(wx.EVT_TEXT, self.check_sequence)
        self.dna_field.Bind(wx.EVT_TEXT_PASTE, self.paste_fasta)
        self.anneal_range_minimum.Bind(
            wx.EVT_SPINCTRL, event_wrapper(self.range_handler,
                                           self.anneal_range_maximum, True))
        self.anneal_range_maximum.Bind(
            wx.EVT_SPINCTRL, event_wrapper(self.range_handler,
                                           self.anneal_range_minimum, False))
        self.target_range_minimum.Bind(
            wx.EVT_SPINCTRL, event_wrapper(self.range_handler,
                                           self.target_range_maximum, True))
        self.target_range_maximum.Bind(
            wx.EVT_SPINCTRL, event_wrapper(self.range_handler,
                                           self.target_range_minimum, False))

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
        sequence = self.dna_field.GetValue()
        sequence = re.sub("[^atcgnxATCGNX]", "", sequence)
        self.dna_field.ChangeValue(sequence)
        if sequence:
            length_seq = len(sequence)
            self.anneal_range_minimum.SetRange(1, length_seq - 1)
            self.anneal_range_maximum.SetRange(2, length_seq)
            self.set_additional_widgets()
            return True
        else:
            self.max_pcr.SetRange(0, 1)
            self.anneal_range_minimum.SetRange(0, 1)
            self.anneal_range_maximum.SetRange(1, 2)
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
            self.dna_field.SetValue(text)
        wx.TheClipboard.Close()

    def set_additional_widgets(self):
        """ Sets the maximum pcr product size according to the range of
        the annealing range. Also limits the range of the target
        """
        self.skip_additional = True
        anneal_range = (self.anneal_range_maximum.GetValue() -
                        self.anneal_range_minimum.GetValue())
        target_range = 0
        if self.use_target.GetValue():
            target_range = (self.target_range_maximum.GetValue() -
                            self.target_range_minimum.GetValue())
        self.max_pcr.SetRange(target_range, anneal_range)
        self.target_range_minimum.SetRange(minimum_range, maximum_range - 1)
        self.target_range_maximum.SetRange(minimum_range + 1, maximum_range)
        self.skip_additional = False

    def range_handler(self, evt, other_widget, add):
        """ Handles the spin events for the anneal_range_minimum,
        anneal_range_maximum, target_range_minimum and
        target_range_maximum widgets. This makes sure that the other
        widget of the range is set appropriately. This is done by
        adding or substracting 1 value, what is determined by the add
        parameter. Also sets the maximum value of the PCR product size
        and correct range for the target range.

        Parameters:
            evt - The wx Spin event
            other_widget - The widget which needs to be checked against
            add - Whether to add or subtract
        Returns:
            -
        """
        value = evt.GetEventObject().GetValue()
        other_value = other_widget.GetValue()
        if other_value >= value and not add:
            other_widget.SetValue(value - 1)
        elif value >= other_value and add:
            other_widget.SetValue(value + 1)
        if not self.skip_additional:
            self.set_additional_widgets()

    ## Panel creation methods

    def create_dna_input(self):
        """ Creates the left side of the GUI, which contains the text
        'Insert template DNA:' and a multiline textfield which should
        only contain the following characters: a, t, c, g, n, x or those
        characters in upper case. This is not enforced here, but is
        implemented on the containing Frame.

        Parameters:
            -
        Returns:
            A BoxSizer containing a text along with a multiline
            textfield.
        """
        # Create the text header, which is centered
        header_box = wx.BoxSizer(wx.HORIZONTAL)
        header_box.Add(wx.StaticText(self, wx.ID_ANY, "Insert template DNA:"), 1,
                       wx.ALIGN_CENTER)
        # Create the input textbox
        self.dna_field = wx.TextCtrl(self, wx.ID_ANY, style=(wx.TE_MULTILINE |
                                                             wx.TE_RICH2 |
                                                             wx.TE_CHARWRAP))
        # Add everything to a box
        dna_input_box = wx.BoxSizer(wx.VERTICAL)
        dna_input_box.Add(header_box, 1, wx.ALIGN_CENTER)
        dna_input_box.Add(self.dna_field, 4, wx.EXPAND)
        return dna_input_box

    def create_settings_box(self):
        """ Creates the right side of the GUI, which contains the
        settings for the primers to be found.

        Parameters:
            -
        Returns:
            A wx.BoxSizer containing all the contents of this side
        """
        input_settings = [{"t": "Max PCR product size", "f": "max_pcr"},
                          {"t": "Annealing range settings"}, {"t": "Minimum",
                          "f": "anneal_range_minimum"}, {"t": "Maximum",
                          "f": "anneal_range_maximum"}]
        self.primers_button = wx.Button(
            self, wx.ID_ANY, label="Search primers")
        settings_box = wx.BoxSizer(wx.VERTICAL)
        settings_box.Add(self.create_widget_box(input_settings), 3, wx.EXPAND)
        settings_box.Add(self.primers_button, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        return settings_box

    def create_optional_input(self):
        """ Creates all the optional settings box which contains all
        optional settings. Those settings are created using
        create_widget_box, except for the target checkbox.

        Parameters:
            -
        Returns:
            A BoxSizer containing the settings
        """
        spinner_settings = [{"t": "Target range settings"},
                            {"t": "Minimum", "f": "target_range_minimum"},
                            {"t": "Maximum", "f": "target_range_maximum"}]
        optional_box = wx.StaticBox(self, wx.ID_ANY, "Optional settings")
        optional_settings = wx.StaticBoxSizer(optional_box, wx.HORIZONTAL)
        left_box = self.create_widget_box(spinner_settings)
        # Add wrappers to add the target checkbox
        entry_box = wx.BoxSizer(wx.HORIZONTAL)
        entry_box.Add(wx.StaticText(self, wx.ID_ANY, "Use target"), wx.EXPAND)
        self.use_target = wx.CheckBox(self, wx.ID_ANY)
        entry_box.Add(self.use_target, wx.EXPAND)
        # Wrap left box in a new vertical box
        wrapper_box = wx.BoxSizer(wx.VERTICAL)
        wrapper_box.Add(left_box, 1, wx.EXPAND)
        wrapper_box.Add(entry_box, 1, wx.EXPAND)
        # Add it to the main box
        optional_settings.Add(wrapper_box, 1, wx.EXPAND)
        checkbox_settings = [{"t": "Experimental dimer checking",
                             "f": "dimer_check"},
                             {"t": "Experimental self dimer checking",
                             "f": "self_dimer_check"},
                             {"t": "Experimental hairpin checking",
                             "f": "hairpin_check"}]
        checkbox_creator = lambda parent: wx.CheckBox(parent, wx.ID_ANY)
        optional_settings.Add(self.create_widget_box(checkbox_settings,
                              checkbox_creator), 1, wx.EXPAND | wx.LEFT, 5)
        return optional_settings

    def create_widget_box(self, configuration, callable=default_spinner):
        """ A method for easily creating a list of text - widget columns.
        This is done with the configuration parameter which determines
        the structure. It is aimed to either create spacers or widgets
        defined by a settings dict.
        The keys of a dictionary within the input settings:
            t: The text which will show to the left of the spin button
            f: The name of the field which would be set to the widget
            on this object.
        When f is not set, it will be considered as a spacer. The
        actual widget which gets created is determined by the
        callable parameter, which refers to a function which
        creates a fresh widget.

        Parameters:
            configuration - A dictionary with the input settings.
            callable - Creates a freshly initialised widget.
        Returns:
            A (new) BoxSizer which contains all the settings.
        """
        # Column for the text
        text_box = wx.BoxSizer(wx.VERTICAL)
        # Column for the actual input
        widget_box = wx.BoxSizer(wx.VERTICAL)
        for input_setting in configuration:
            text = wx.StaticText(self, wx.ID_ANY, input_setting["t"])
            horizontal_wrapper = wx.BoxSizer(wx.HORIZONTAL)
            horizontal_wrapper.Add(text, 1, wx.ALIGN_CENTER)
            text_box.Add(horizontal_wrapper, 1, wx.ALIGN_LEFT)
            widget = (0, 0)
            # Add a spacer when this is shouldn't be a spinner
            if "f" in input_setting:
                widget = callable(self)
                setattr(self, input_setting["f"], widget)
            widget_box.Add(widget, 1, wx.ALIGN_RIGHT)
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(text_box, 1, wx.EXPAND)
        main_box.Add(widget_box, 1, wx.EXPAND)
        return main_box
