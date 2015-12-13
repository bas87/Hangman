#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import random
import wx
import i18n
from dic import WordReader

# Globals
def _(t): return i18n.language.gettext(t).decode('utf8')


class GameWindow(wx.Window):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.Window.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(wx.NamedColour('white'))

        # Windows platform excaption
        if wx.Platform == '__WXGTK__':
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        else:
            self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)

        self.SetFocus()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        self.Refresh()

        
    def StartGame(self, word):
        # Init defaults values
        self.word = word
        self.guess = []
        self.tries = 0
        self.misses = 0
        
        _tmp_word = u''.join(set(word))
        if len(_tmp_word) > 1:
            self.hint = u''.join(random.sample(_tmp_word, int(len(_tmp_word)*0.4)))
        else:
        	self.hint = _tmp_word

        # Draw picture
        self.Draw()


    def EndGame(self):
        self.misses = 7 # reset to default attempts
        self.guess = map(chr, range(ord('a'),ord('z')+1))
        self.Draw()


    def HandleKey(self, key):
        self.message = ""
        if self.guess.count(key):
            self.message = _(u'Already guessed: %s') % (key,)
            return 0

        self.guess.append(key)
        self.guess.sort()
        self.tries = self.tries+1

        if not key in self.word:
            self.misses = self.misses+1

        if self.misses == 7:
            self.EndGame()
            return 1

        has_won = 1
        for letter in self.word:
            if not self.guess.count(letter):
                has_won = 0
                break

        if has_won:
            self.Draw()
            return 2

        self.Draw()

        return 0


    def Draw(self, dc = None):
        if not dc:
            dc = wx.ClientDC(self)

        dc.SetFont(self.font)
        dc.Clear()

        (x,y) = self.GetSizeTuple()

        x1 = x-170
        y1 = 20

        for letter in self.word:
            if self.guess.count(letter):
                dc.DrawText(letter, x1, y1)
            else:
                dc.DrawText('.', x1, y1)
            x1 = x1 + 10

        x1 = x-170
        dc.DrawText(_(u'tries %d misses %d') % (self.tries,self.misses),x1,50)

        guesses = ''
        for letter in self.guess:
            guesses = guesses + letter

        dc.DrawText(_(u'hint: ') + self.hint, x1, 70)
        dc.DrawText(_(u'guessed: '), x1, 90)
        dc.DrawText(guesses[:13], x1+80, 90)
        dc.DrawText(guesses[13:], x1+80, 110)
        dc.SetUserScale(x/1000.0, y/1000.0)

        self.DrawVictim(dc)


    def DrawVictim(self, dc):
        dc.SetPen(wx.Pen(wx.Colour(168,89,39), 20))
        dc.DrawLines([(10, 980), (10,900), (700,900), (700,980)])
        dc.DrawLines([(100,900), (100, 100), (300,100)])
        dc.DrawLine(100,200,200,100)

        if ( self.misses == 0 ): return
        dc.SetPen(wx.Pen(wx.Colour(245,212,29), 10))
        dc.DrawLine(300,100,300,200)
        dc.SetPen(wx.Pen(wx.NamedColour('black'), 10))

        if ( self.misses == 1 ): return
        dc.DrawEllipse(250,200,100,100)
        dc.DrawEllipse(280, 230, 10, 10)
        dc.DrawEllipse(310, 230, 10, 10)

        if ( self.misses == 2 ): return
        dc.DrawLine(300,300,300,600)

        if ( self.misses == 3) : return
        dc.DrawLine(300,300,250,550)

        if ( self.misses == 4) : return
        dc.DrawLine(300,300,350,550)

        if ( self.misses == 5) : return
        dc.DrawLine(300,600,350,840)

        if ( self.misses == 6) : return
        dc.DrawLine(300,600,250,840)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.Draw(dc)


class GameFrame(wx.Frame):
    def __init__(self, parent, wr):
        self.wr = wr
        wx.Frame.__init__(self, parent, wx.ID_ANY, _(u'Hangman'), wx.DefaultPosition, (500,600))
        self.SetBackgroundColour(wx.NamedColour('white'))

        # main sizer
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        v_sizer = wx.BoxSizer( wx.VERTICAL )

        # Game Panel
        self.wnd = GameWindow(self, wx.ID_ANY)
        v_sizer.Add(self.wnd, 1, wx.EXPAND | wx.ALL, 6 )

        # Grid sizer for vitrual keyboard
        g_sizer = wx.GridSizer(0, 8, 0, 0)

        # Set buttons to sizer
        for i in range(ord('a'), ord('z')+1):
            button = wx.Button(self, 1005, chr(i), wx.DefaultPosition, wx.DefaultSize, 0)
            button.SetMinSize(wx.Size( 50,50 ))
            g_sizer.Add(button, 0, wx.ALL, 5 )

        v_sizer.Add(g_sizer, 1, wx.EXPAND, 5)

        # Menu bar
        menubar = wx.MenuBar()

        # Game menu
        menu = wx.Menu()

        new = wx.MenuItem(menu, 1001, _(u'&New\tCtrl+N'), _(u'New Game'))
        menu.AppendItem(new)

        end = wx.MenuItem(menu, 1002, _(u'&End\tCtrl+E'), _(u'End Game'))
        menu.AppendItem(end)

        menu.AppendSeparator()

        reset = wx.MenuItem(menu, 1003, _(u'&Reset\tCtrl+R'), _(u'Reset Rame'))
        menu.AppendItem(reset)

        menu.AppendSeparator()

        quit = wx.MenuItem(menu, 1004, _(u'&Quit\tCtrl+Q'), _(u'Quit the Application'))
        menu.AppendItem(quit)

        menubar.Append(menu, _(u'Game'))

        # Dic menu
        urlmenu = wx.Menu()

        self.dics = [ u'Česky', 'dic/cs.txt',
                 u'Česky - Demo', 'dic/cs_demo.txt',
                 u'English', 'dic/en.txt']

        for item in range(0,len(self.dics),2):
            urlmenu.Append(1020+item/2, self.dics[item], self.dics[item+1])

        menubar.Append(urlmenu, _(u'Dictionary'))
        self.SetMenuBar(menubar)

        self.SetSizer(v_sizer)
        self.Layout()

        # Two col status bar
        self.CreateStatusBar(2)

        # Bind events
        self.Bind(wx.EVT_MENU, self.OnGameNew, id=1001)
        self.Bind(wx.EVT_MENU, self.OnGameEnd, id=1002)
        self.Bind(wx.EVT_MENU, self.OnGameReset, id=1003)
        self.Bind(wx.EVT_MENU, self.OnWindowClose, id=1004)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=1005)
        self.Bind(wx.EVT_MENU, self.OnSelectDic, id=1020, id2=1020+len(self.dics)/2)
        self.wnd.Bind(wx.EVT_CHAR, self.OnChar)

        self.Centre(wx.BOTH)

        self.OnGameReset()


    def OnGameNew(self, event):
        word = self.wr.Get()
        self.in_progress = 1
        self.SetStatusText("",0)
        self.wnd.StartGame(word)


    def OnGameEnd(self, event):
        self.UpdateAverages(0)
        self.in_progress = 0
        self.SetStatusText("",0)
        self.wnd.EndGame()


    def OnGameReset(self, event=None):
        self.played = 0
        self.won = 0
        self.history = []
        self.average = 0.0
        self.OnGameNew(None)


    def OnSelectDic(self, event):
        item = (event.GetId() - 1020)*2
        self.wr = WordReader(self.dics[item+1])
        self.OnGameNew(None)


    def UpdateAverages(self, has_won):
        if has_won:
            self.won = self.won + 1

        self.played = self.played+1
        self.history.append(self.wnd.misses) # ugly

        total = 0.0
        for m in self.history:
            total = total + m

        self.average = float(total/len(self.history))


    def OnButton(self, event):
        self.wnd.SetFocus()
        btn = event.GetEventObject()
        self.HandleKey(ord(btn.GetLabelText()));


    def OnChar(self, event):
        self.wnd.SetFocus()
        key = event.GetKeyCode()
        def cb():
            event.Skip()
        self.HandleKey(key, cb)


    def OnWindowClose(self, event):
        dlg = wx.MessageDialog(self, _(u'Do you want close this window?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
        val = dlg.ShowModal()

        if val == wx.ID_YES:
            wx.Exit()
        elif val == wx.ID_CANCEL:
            dlg.Destroy()

    def HandleKey(self, key, skip = None):

        if not self.in_progress:
            self.OnGameNew(None)
            return

        if key >= ord('A') and key <= ord('Z'):
            key = key + ord('a') - ord('A')
        key = chr(key)

        if key < 'a' or key > 'z':
            if not None:
                skip()
            return

        res = self.wnd.HandleKey(key)
        if res == 0:
            self.SetStatusText(self.wnd.message)
        elif res == 1:
            self.UpdateAverages(0)
            self.in_progress = 0

            dlg = wx.MessageDialog(self, _(u'Too bad, you\'re dead!'), '', wx.OK | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                self.OnGameNew(None)

        elif res == 2:
            self.in_progress = 0
            self.UpdateAverages(1)

            dlg = wx.MessageDialog(self, _(u'Congratulations! You\'re alive!'), '', wx.OK | wx.ICON_INFORMATION)
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                self.OnGameNew(None)

        if self.played:
            percent = (100.*self.won)/self.played
        else:
            percent = 0.0
        self.SetStatusText(_(u'played %d, won %d (%g %%)') % (self.played,self.won, round(percent)),1)


class GameApp(wx.App):
    def OnInit(self):
        wr = WordReader('dic/cs_demo.txt')
        frame = GameFrame(None, wr)
        self.SetTopWindow(frame)
        frame.Show()
        return True


# Start main loop
if __name__ == '__main__':
    app = GameApp(0)
    app.MainLoop()