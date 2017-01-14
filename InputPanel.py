import wx


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
        required_input = wx.BoxSizer(wx.HORIZONTAL)
        required_input.Add(self.create_dna_input(), 1, wx.EXPAND)
        required_input.Add(self.create_settings_box(), 1, wx.EXPAND | wx.LEFT,
                           5)
        padding_box = wx.BoxSizer(wx.VERTICAL)
        padding_box.Add(required_input, 1, wx.EXPAND | wx.ALL, 5)
        padding_box.Add(self.create_optional_input(), 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(padding_box)

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
        create_widget_box.

        Parameters:
            -
        Returns:
            A BoxSizer containing the settings
        """
        spinner_settings = [{"t": "Target range settings"},
                            {"t": "Minimum", "f": "target_range_minimum"},
                            {"t": "Maximum", "f": "target_range_minimum"}]
        optional_box = wx.StaticBox(self, wx.ID_ANY, "Optional settings")
        optional_settings = wx.StaticBoxSizer(optional_box, wx.HORIZONTAL)
        optional_settings.Add(self.create_widget_box(spinner_settings), 2,
                              wx.EXPAND)
        checkbox_settings = [{"t": "Experimental dimer checking",
                             "f": "dimer_check"},
                             {"t": "Experimental self dimer checking",
                             "f": "self_dimer_check"},
                             {"t": "Experimental hairpin checking",
                             "f": "hairpin_check"}]
        checkbox_creator = lambda parent: wx.CheckBox(parent, wx.ID_ANY)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
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
