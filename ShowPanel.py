import wx
import wx.lib.scrolledpanel as scrolled


class ShowPanel(wx.Panel):

    def __init__(self, parent, id):
        super(ShowPanel, self).__init__(parent, id)
        self.button = wx.Button(self, label="Return")
        self.main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main)

    def set_primers(self, primers):
        self.main.Clear(True)
        combinations = self.preprocess_found_data(primers)
        layout = self.create_combination_layout(combinations)
        self.main.Add(layout, 3, wx.EXPAND)
        self.main.Add(self.button, 1, wx.CENTER)

    def preprocess_found_data(self, primers):
        combinations = []
        for primer_match in primers:
            fprimer = primer_match["primer"]
            fprimer["position"] = "{}..{}".format(*fprimer["position"])
            for rprimer in primer_match["rprimers"]:
                rprimer["pcr"] = len(rprimer["pcr"])
                rprimer["position"] = "{}..{}".format(*rprimer["position"])
                combinations.append((fprimer, rprimer))
        return combinations

    def create_combination_layout(self, combinations):
        combination_box = wx.BoxSizer(wx.VERTICAL)
        self.scroll_panel = scrolled.ScrolledPanel(
            self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        for combination in combinations:
            single = self.create_combination(combination)
            combination_box.Add(single, 1, wx.EXPAND)
        self.scroll_panel.SetSizer(combination_box)
        return self.scroll_panel

    def create_combination(self, combination):
        border_box = wx.StaticBox(self, wx.ID_ANY, "")
        content_box = wx.StaticBoxSizer(border_box, wx.VERTICAL)
        content_box.Add(self.layer(combination, "seq"), 1, wx.EXPAND)
        content_box.Add(self.layer(combination, "melt_temp",
                                   "Melting temperature:"), 1, wx.EXPAND)
        content_box.Add(self.layer(combination, "gc_perc", "GC%:"), 1,
                        wx.EXPAND)
        content_box.Add(self.layer(combination, "position", "Position:"), 1,
                        wx.EXPAND)
        # Add the PCR box manually, with a tiny hack
        content_box.Add(self.layer([{"x": combination[1]["pcr"]}, {"x": ""}],
                                   "x", "PCR product:"), 1, wx.EXPAND)
        return content_box

    def layer(self, combination, key, name=""):
        horizontal_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        name_widget = (wx.StaticText(self.scroll_panel, wx.ID_ANY, name)
                       if name else (0, 0))
        horizontal_wrapper.Add(name_widget, 1, wx.EXPAND)
        widget0 = wx.StaticText(self.scroll_panel, wx.ID_ANY,
                                str(combination[0][key]))
        widget1 = wx.StaticText(self.scroll_panel, wx.ID_ANY,
                                str(combination[1][key]))
        horizontal_wrapper.Add(widget0, 1, wx.EXPAND)
        horizontal_wrapper.Add(widget1, 1, wx.EXPAND)
        return horizontal_wrapper
