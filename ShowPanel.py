import wx


class ShowPanel(wx.Panel):

    def __init__(self, parent, id):
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
            self.main_sizer.Prepend(center_text_wrapper, 1, wx.EXPAND |
                                    wx.ALIGN_CENTER)
            self.main_sizer.Prepend((0, 0), 1, wx.EXPAND)
        self.main_sizer.Layout()

    def create_primer_box(self, primer, fpr):
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
        if args or kwargs:
            text = text.format(*args, **kwargs)
        return wx.StaticText(self, wx.ID_ANY, text)
