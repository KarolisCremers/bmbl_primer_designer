import wx
import re
from InputPanel import InputPanel


class Frame(wx.Frame):
    
    def __init__(self, parent, id, title):
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
        self.input_panel.dna_field.Bind(wx.EVT_TEXT, self.check_sequence)
        self.input_panel.dna_field.Bind(wx.EVT_TEXT_PASTE, self.paste_fasta)
        self.input_panel.max_target.Bind(wx.EVT_SPIN, self.target_handler)
        self.input_panel.range_minimum.Bind(wx.EVT_SPIN, self.minimum_handler)
        self.input_panel.range_maximum.Bind(wx.EVT_SPIN, self.maximum_handler) 
    
    def check_sequence(self, *args):
        print("2")
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
        if not self.usr_target:
            self.usr_target = True

    def minimum_handler(self, evt):
        value = evt.GetEventObject().GetValue()
        if value >= self.input_panel.range_maximum.GetValue():
            self.input_panel.range_maximum.SetValue(value + 1)

    def maximum_handler(self, evt):
        value = evt.GetEventObject().GetValue()
        if value <= self.input_panel.range_minimum.GetValue():
            self.input_panel.range_minimum.SetValue(value - 1)
            

if __name__ == '__main__':
    app = wx.App()
    Frame(None, -1, "Simple primer designer")
    app.MainLoop()
    
