import wx


class ShowPanel(wx.Panel):

    def __init__(self, parent, id):
        """ Creates the panel which contains the primer information.
        Contains a sizer of which the first two elements are
        placeholders for primer info or a text displaying
        'no primers found'
        This panel is initially hidden.
        """

        super(ShowPanel, self).__init__(parent, id)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add((0, 0), 1, wx.EXPAND)
        self.main_sizer.Add((0, 0), 1, wx.EXPAND)
        self.return_button = wx.Button(self, wx.ID_ANY,
                                       label="Return to settings")
        self.main_sizer.Add(self.return_button, 1, wx.EXPAND)
        self.SetSizer(self.main_sizer)
        self.Hide()

    def set_primer(self, primer_match):
        """ Sets the primer match for this panel. If no primer_match is
        available a text will be displayed.

        Parameters:
             primer_match - The match object to get the primers from
        """
        self.main_sizer.Remove(1)
        self.main_sizer.Remove(0)
        if primer_match:
            title_box = wx.BoxSizer(wx.VERTICAL)
            for text in "", "Sequence:", "Melt temp:", "GC%:", "Position:":
                title_box.Add(self.create_text(text), 1, wx.EXPAND)
            column_box = wx.BoxSizer(wx.HORIZONTAL)
            column_box.Add(title_box, 1, wx.EXPAND)
            column_box.Add(self.create_primer_box(primer_match['fprimer'], True),
                           1, wx.EXPAND)
            column_box.Add(self.create_primer_box(primer_match['rprimer'], False),
                           1, wx.EXPAND)
            pcr_box = wx.BoxSizer(wx.HORIZONTAL)
            pcr_box.Add(self.create_text("PCR:"), 1, wx.EXPAND)
            pcr_box.Add(self.create_text(str(len(primer_match['pcr']))), 1,
                        wx.EXPAND)
            pcr_box.Add((0, 0), 1, wx.EXPAND)
            self.main_sizer.Prepend(pcr_box, 1, wx.EXPAND)
            self.main_sizer.Prepend(column_box, 2, wx.EXPAND)
        else:
            center_text_wrapper = wx.BoxSizer(wx.HORIZONTAL)
            center_text_wrapper.Add(self.create_text("No primers found"), 1,
                                    wx.EXPAND | wx.ALIGN_CENTER)
            self.main_sizer.Prepend(center_text_wrapper, 1, wx.ALIGN_CENTER)
            self.main_sizer.Prepend((0, 0), 1, wx.EXPAND)
        self.main_sizer.Layout()

    def create_primer_box(self, primer, fpr):
        """ Creates a box for the primer information.

        Parameters:
            primer - The primer to display information from
            fpr - A boolean to indicate whether this is the forward
            primer.
        Returns:
            A BoxSizer containing this information
        """
        primer_box = wx.BoxSizer(wx.VERTICAL)
        primer["position"] = "{}..{}".format(*primer["position"])
        primer_box.Add(
            self.create_text("Forward primer" if fpr else "Reverse primer"), 1,
            wx.EXPAND)
        for format, key in (("5'-{}-3'", "seq"), ("{}C", "melt_temp"),
                            ("{}%", "gc_perc"), ("{}", "position")):
            primer_box.Add(self.create_text(format, str(primer[key])), 1, wx.EXPAND)
        return primer_box

    def create_text(self, text, *args, **kwargs):
        """ Creates a StaticText and formats the text if any arguments
        are given.

        Parameters:
            text - The text to display and format
            *args - Arguments to format the text
            **kwargs - named arguments to format the text
        Returns:
            A StaticText
        """
        if args or kwargs:
            text = text.format(*args, **kwargs)
        return wx.StaticText(self, wx.ID_ANY, text)
