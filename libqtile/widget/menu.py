from .. import bar, manager, drawer, window, hook
import base
import button

class _MenuMarkup():
	def __init__(self, names, entries):
		self.names = names
		self.entries = entries

class _MenuCommand():
	def __init__(self, name, function):
		self.name = name
		self.function = function

class _Menu(base._Widget):
	defaults = manager.Defaults()
	def __init__(self, menu=None):
		self.menu=menu
		self.buttons = []
		for i in xrange(len(self.menu.names)):
			self.buttons.append(_MenuButton(self.menu.names[i],self.menu.entries[i],self))
		base._Widget.__init__(self, bar.CALCULATED)
	def _configure(self, qtile, bar):
		self.qtile, self.bar = qtile, bar
		self.drawer = drawer.Drawer(
							self.qtile,
							self.win.wid,
							self.bar.width,
							self.bar.height
					  )
		w = 0
		for i in self.buttons:
			i._configure(qtile, bar)
			i.set_draweroffset((self.offset or 0)+w)
			w += i.width
	def calculate_width(self):
		self.zones = []
		w = 0
		for i in self.buttons:
			self.zones.append(w)
			w+=i.calculate_width()
		return w
	def draw(self):
		#self.drawer.clear(self.bar.background)
		self.drawer.clear("dd34cc")
		off = 0
		for i in self.buttons:
			i.drawer.clear(i.background)
			i.layout.draw(
				i.actual_padding or 0,
				int(i.bar.height / 2.0 - i.layout.height / 2.0)
			  )
			i.drawer.draw(off, i.calculate_width())
			off = off + i.calculate_width()
	def click(self, x, y , button):
		self.calculate_width()
		i = 0
		while i<len(self.buttons)-1:
			if x>self.zones[i+1]:
				i+=1
			else:
				break
		self.buttons[i].click((self.zones[i]),y,button)

class _MenuButton(button._Button):
	defaults = manager.Defaults(
		("font", "Arial", "Menu font"),
		("fontsize", None, "Menu pixel size. Calculated if None."),
		("padding", 7, "Menu padding. Calculated if None."),
		("background", "000000", "Background colour"),
		("foreground", "ffffff", "Foreground colour")
	)
	def __init__(self, name=None, submenu=None, parent=None):
		self.name = name
		self.submenu = submenu
		self.parent = parent or []
		self.buttons = []
		button._Button.__init__(self, self.name, bar.CALCULATED, self.open_submenu)
		for i in self.submenu:
			k = _MenuEntry(i)
			self.buttons.append(k)
		self.mdrawer = _MenuDrawer(0,0,0,0)
		self.b = False
	def set_draweroffset(self, x):
		self.mdrawer = _MenuDrawer(x, 30, 300, 100)
		self.mdrawer._configure(self.qtile, self.bar.screen)
		for i in self.buttons:
			i._configure(self.qtile, self.mdrawer)
		self.mdrawer.addwidgets(self.buttons)
	def open_submenu(self, x, y, butto):
		print self.bar.screen.x, self.bar.screen.y, self.bar.screen.width, self.bar.screen.height
		for i in self.parent.buttons:
			if i!=self and hasattr(i, 'mdrawer') and i.mdrawer.visible:
				self.b = True
				i.b = not i.b
				i.mdrawer.set_visible(False)
		self.mdrawer.set_visible(self.b)
		self.b = not self.b
	def draw(self):
		self.drawer.clear(self.background or self.bar.background)
		self.layout.draw(
			self.actual_padding or 0,
			int(self.bar.height / 2.0 - self.layout.height / 2.0)
		)
		self.drawer.draw(self.offset, self.width)

class _MenuEntry(base._TextBox):
	defaults = manager.Defaults(
		("font", "Arial", "Main font"),
		("fontsize", 10, "Font size. Calculated if None."),
		("padding", None, "Padding Calculated if None."),
		("background", "000000", "Background colour"),
		("foreground", "ffffff", "Foreground colour")
	)
	def click(self, x, y, button):
		print "clicked"

##Make a debian/gnome menu class which opens programs like the gnome2 menu##
class SampleMenu(_Menu):
	def __init__(self):
		_Menu.__init__(self, _MenuMarkup(["ab","b"],["a","b"]))

class _MenuDrawer(bar._AnywhereBar):
	def handle_ButtonPress(self, e):
		print self.widgets
