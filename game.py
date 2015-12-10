#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import random
import wx
import i18n
from dic import WordReader

# Globals
_ = i18n.language.gettext


class GamePanel(wx.Panel):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(wx.NamedColour('white'))

        # Windows platform excaption
        if wx.Platform == '__WXGTK__':
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        else:
            self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)

        #self.SetFocus()
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
        self.hint = u''.join(random.sample(word, int(len(word)*0.35)))

        # Draw picture
        self.Draw()


    def EndGame(self):
        self.misses = 7 # reset to default attempts
        self.guess = map(chr, range(ord('a'),ord('z')+1))
        self.Draw()


    def HandleKey(self, key):
        self.message = ""
        if self.guess.count(key):
            self.message = _(u'Already guessed %s') % (key,)
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

        x1 = x-200
        y1 = 20

        for letter in self.word:
            if self.guess.count(letter):
                dc.DrawText(letter, x1, y1)
            else:
                dc.DrawText('.', x1, y1)
            x1 = x1 + 10

        x1 = x-200
        dc.DrawText(_('tries %d misses %d').decode('utf8') % (self.tries,self.misses),x1,50)

        guesses = ''
        for letter in self.guess:
            guesses = guesses + letter

        dc.DrawText(_('hint: ').decode('utf8') + self.hint, x1, 70)
        dc.DrawText(_('guessed:').decode('utf8'), x1, 90)
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

        self.pnl = GamePanel(self, wx.ID_ANY)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )


        bSizer1.Add(self.pnl, 1, wx.EXPAND |wx.ALL, 6 )

        gSizer1 = wx.GridSizer( 0, 8, 0, 0 )

        for i in range(ord('a'), ord('z')+1):
            m_button8 = wx.Button( self, 1006, chr(i), wx.DefaultPosition, wx.DefaultSize, 0 )
            m_button8.SetMinSize( wx.Size( 50,50 ) )

            gSizer1.Add(m_button8, 0, wx.ALL, 5 )

        bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )


        menu = wx.Menu()
        menu.Append(1001, _('New'))
        menu.Append(1002, _(u'End'))
        menu.AppendSeparator()
        menu.Append(1003, _(u'Reset'))
        menu.AppendSeparator()

        quit = wx.MenuItem(menu, 1005, '&Quit\tCtrl+Q', _(u'Quit the Application'))
        menu.AppendItem(quit)

        #menu.Append(1005, "Exit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "Game")
        menu = wx.Menu()
        urls = [ u'Česky', 'dic/cs.txt',
        		 u'Česky - Demo', 'dic/cs_demo.txt',
        		 u'English', 'dic/en.txt']
        urlmenu = wx.Menu()
        for item in range(0,len(urls),2):
            menu.Append(1020+item/2, urls[item], urls[item+1])
        menubar.Append(menu, _(u'Dictionary'))
        self.urls = urls
        self.urloffset = 1020
        self.SetMenuBar(menubar)

        self.SetSizer( bSizer1 )
        self.Layout()


        self.CreateStatusBar(2)
        self.Bind(wx.EVT_MENU, self.OnGameNew, id=1001)
        self.Bind(wx.EVT_MENU, self.OnGameEnd, id=1002)
        self.Bind(wx.EVT_MENU, self.OnGameReset, id=1003)
        self.Bind(wx.EVT_MENU, self.OnWindowClose, id=1005)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=1006)
        self.Bind(wx.EVT_MENU, self.OnSelectDic, id=1020, id2=1020+len(urls)/2)
        self.pnl.Bind(wx.EVT_CHAR, self.OnChar)
        self.OnGameReset()

        self.Centre( wx.BOTH )

    def OnGameNew(self, event):
        word = self.wr.Get()
        self.in_progress = 1
        self.SetStatusText("",0)
        self.pnl.StartGame(word)

    def OnGameEnd(self, event):
        self.UpdateAverages(0)
        self.in_progress = 0
        self.SetStatusText("",0)
        self.pnl.EndGame()

    def OnGameReset(self, event=None):
        self.played = 0
        self.won = 0
        self.history = []
        self.average = 0.0
        self.OnGameNew(None)

    def OnSelectDic(self, event):
        item = (event.GetId() - self.urloffset)*2
        print "Trying to load %s" % (self.urls[item+1])
        self.wr = WordReader(self.urls[item+1])

    def UpdateAverages(self, has_won):
        if has_won:
            self.won = self.won + 1
        self.played = self.played+1
        self.history.append(self.pnl.misses) # ugly
        total = 0.0
        for m in self.history:
            total = total + m
        self.average = float(total/len(self.history))

    def OnButton(self, event):
        btn = event.GetEventObject()
        print self.HandleKey(ord(btn.GetLabelText()));

        #print btn.GetLabelText()

    def OnChar(self, event):
        if not self.in_progress:
            #print "new"
            self.OnGameNew(None)
            return
        key = event.GetKeyCode();
        #print key
        if key >= ord('A') and key <= ord('Z'):
            key = key + ord('a') - ord('A')
        key = chr(key)
        if key < 'a' or key > 'z':
            event.Skip()
            return
        res = self.pnl.HandleKey(key)
        if res == 0:
            self.SetStatusText(self.pnl.message)
        elif res == 1:
            self.UpdateAverages(0)
            self.SetStatusText(_(u'Too bad, you\'re dead!'),0)
            self.in_progress = 0
        elif res == 2:
            self.in_progress = 0
            self.UpdateAverages(1)
            self.SetStatusText(_(u'Congratulations!'),0)
        if self.played:
            percent = (100.*self.won)/self.played
        else:
            percent = 0.0
        self.SetStatusText(_(u'p %d, w %d (%g %%), av %g') % (self.played,self.won, percent, self.average),1)

    def OnWindowClose(self, event):
        dlg = wx.MessageDialog(self, _(u'Do you want close this window?'), '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)
        val = dlg.ShowModal()

        if val == wx.ID_YES:
            wx.Exit()
        elif val == wx.ID_CANCEL:
            dlg.Destroy()

    def HandleKey(self, key):
        if not self.in_progress:
            #print "new"
            self.OnGameNew(None)
            return

        #print key

        if key >= ord('A') and key <= ord('Z'):
            key = key + ord('a') - ord('A')
        key = chr(key)
        if key < 'a' or key > 'z':
            #event.Skip()
            return
        res = self.pnl.HandleKey(key)
        if res == 0:
            self.SetStatusText(self.pnl.message)
        elif res == 1:
            self.UpdateAverages(0)
            self.SetStatusText("Too bad, you're dead!",0)
            self.in_progress = 0
        elif res == 2:
            self.in_progress = 0
            self.UpdateAverages(1)
            self.SetStatusText("Congratulations!",0)
        if self.played:
            percent = (100.*self.won)/self.played
        else:
            percent = 0.0
        self.SetStatusText(_(u'p %d, w %d (%g %%), av %g') % (self.played,self.won, percent, self.average),1)



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