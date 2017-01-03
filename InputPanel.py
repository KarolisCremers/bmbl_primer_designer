import wx


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
        #create_dna_input and #create_settings_box to fill this
        container. Then this containeR is put in another container
        which makes sure there are 5 pixels around the border.

        Parameters:
            parent - The parent wx Object for this panel.
            id - The id this panel should have.
        Returns:
            -
        """
        super(InputPanel, self).__init__(parent, id)
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        main_box.Add(self.create_dna_input(), 1, wx.EXPAND)
        main_box.Add(self.create_settings_box(), 1, wx.EXPAND | wx.LEFT, 5)
        padding_box = wx.BoxSizer()
        padding_box.Add(main_box, 1, wx.EXPAND | wx.ALL, 5)
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
        header_box.Add(wx.StaticText(self, -1, "Insert template DNA:"), 1,
                       wx.ALIGN_CENTER)
        # Create the input textbox
        self.dna_field = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE |
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
        self.primers_button = wx.Button(self, -1, label="Search primers")
        settings_box = wx.BoxSizer(wx.VERTICAL)
        settings_box.Add(self.create_input_settings(), 3, wx.EXPAND)
        settings_box.Add(self.primers_button, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        return settings_box

    def create_input_settings(self, main_box=wx.BoxSizer(wx.HORIZONTAL)):
        """ A method for easily creating settings through the
        input_settings list in this method. It is aimed to either
        create spacers or SpinButtons defined by a settings dict.
        The keys of a dictionary within the input settings:
            t: The text which will show to the left of the spin button
            s: The name of the field which would be set to the widget
            on this object.
            sp: A boolean value whether this is a spacer or SpinButton.

        Parameters:
            main_box - A BoxSizer which will contain the settings. By
            default this is a horizontal box sizer.
        Returns:
            A (new) BoxSizer which contains all the settings.
        """
        input_settings = [{"t": "Max PCR product size", "s": "max_target",
                          "sp": True}, {"t": "Range settings",
                          "sp": False}, {"t": "Minimum", "s": "range_minimum",
                          "sp": True}, {"t": "Maximum", "s": "range_maximum",
                          "sp": True}]
        # Column for the text
        text_box = wx.BoxSizer(wx.VERTICAL)
        # Column for the actual input
        spinner_box = wx.BoxSizer(wx.VERTICAL)
        for input_setting in input_settings:
            text = wx.StaticText(self, -1, input_setting["t"])
            text_box.Add(text, 1, wx.ALIGN_LEFT)
            spin = (0, 0)
            # Add a spacer when this is shouldn't be a spinner
            if input_setting["sp"]:
                spin = wx.SpinButton(self, -1,
                                     style=InputPanel.SPINNER_STYLE)
                spin.SetRange(0, pow(2, 31) - 1)
                setattr(self, input_setting["s"], spin)
            spinner_box.Add(spin, 1, wx.EXPAND)
        main_box.Add(text_box, 1, wx.EXPAND)
        main_box.Add(spinner_box, 1, wx.EXPAND)
        return main_box

