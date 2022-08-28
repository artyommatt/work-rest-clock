from os.path import exists
import datetime
import time

import wx


class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(450, 270), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gbSizer1 = wx.GridBagSizer(3, 3)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"00:00:00", wx.Point(50, 50), wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        self.m_staticText1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                                           wx.EmptyString))
        gbSizer1.Add(self.m_staticText1, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"00:00:00", wx.Point(200, 100), wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                                           wx.EmptyString))
        gbSizer1.Add(self.m_staticText2, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Время занятия", wx.Point(50, 50), wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gbSizer1.Add(self.m_staticText3, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Время отдыха", wx.Point(50, 50), wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gbSizer1.Add(self.m_staticText4, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Старт", wx.DefaultPosition, wx.Size(120, 50), 0)
        gbSizer1.Add(self.m_button1, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        self.Bind(wx.EVT_BUTTON, self.on_button1, self.m_button1)

        gbSizer1.AddGrowableCol(2)
        gbSizer1.AddGrowableRow(2)

        bSizer1.Add(gbSizer1, 1, wx.SHAPED, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Учет времени", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Сохраненное", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)

        self.m_menuItem3 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Напоминания", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)

        self.m_menu1.AppendSeparator()

        self.m_menuItem4 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Выход\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem4)
        self.Bind(wx.EVT_MENU, self.on_quit, self.m_menuItem4)

        self.m_menubar1.Append(self.m_menu1, u"Меню")

        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)

        # создаем объект таймера обновления
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        self.sw1 = wx.StopWatch()
        self.sw2 = wx.StopWatch()

        self.Bind(wx.EVT_CLOSE, self.on_quit)

    def __del__(self):
        pass

    # Реализация нажатия на кнопку
    def on_button1(self, event):
        btn_label = self.m_button1.GetLabel()
        if btn_label == "Старт":
            self.timer.Start(100)
            self.sw1.Start()
            self.sw2.Start()
            self.sw2.Pause()
            self.m_button1.SetLabel("Отдыхать")
        elif btn_label == "Отдыхать":
            self.sw1.Pause()
            self.sw2.Resume()
            self.m_button1.SetLabel("Заниматься")
        elif btn_label == "Заниматься":
            self.sw2.Pause()
            self.sw1.Resume()
            self.m_button1.SetLabel("Отдыхать")

    def on_quit(self, event):
        self.save_result()
        self.Destroy()

    # обновляем название по таймеру и выводим время на экран
    def update(self, event):
        sec1 = self.sw1.Time() / 1000
        sec2 = self.sw2.Time() / 1000
        self.m_staticText1.SetLabel(time.strftime("%H:%M:%S", time.gmtime(sec1)))
        self.m_staticText2.SetLabel(time.strftime("%H:%M:%S", time.gmtime(sec2)))

        # Вывод текущего времени в статусбар (будет отображаться после запуска времени)
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%d/%m/%Y  %H:%M")
        self.m_statusBar1.SetStatusText(dt_str)

    def save_result(self):
        if exists('saves.txt'):
            pass
        else:
            with open("saves.txt", "w+") as f:
                f.write('log is starting\n')
        date = datetime.date.today()
        date_str = date.strftime('%d/%m/%Y')
        with open("saves.txt", "r") as f:
            last_string = f.readlines()[-1].split(sep=", ")
        if last_string[0] == date_str:
            sum_msec = int(last_string[1]) + self.sw1.Time()
            last_string.pop(1)
            last_string.insert(1, str(sum_msec))

            with open("saves.txt", "r") as f:
                old_data = f.read()

            with open("saves.txt", "r") as f:
                new_data = old_data.replace(f"{f.readlines()[-1]}", f"{', '.join(last_string)}")

            with open("saves.txt", "w") as f:
                f.write(new_data)
        else:
            with open("saves.txt", "a") as f:
                f.write(f"{date_str}, {self.sw1.Time()}, \n")


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame1(None)
    frame.Show()
    app.MainLoop()
