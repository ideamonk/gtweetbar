#!/usr/bin/env python

INSTALL_PATH = "/usr/share/gtweetbar"

import pygtk
pygtk.require("2.0")
import gtk
import gnomeapplet

# make local copy of twitter api importable
import sys
sys.path.append(INSTALL_PATH + '/python_twitter')
import twitter


class TweetBar(object):

	username = "username"
	password = "***"
	oldTweet = ""
	MaxChars = 140
	
	def __init__(self,applet):
		self.api = twitter.Api()
		
		# lets save a reference for future use
		self.applet = applet
		self.applet.connect("change-size", self.on_change_size)
		self.applet.connect("change-background", self.change_background)
        
		# interface build up
		self.applet.set_background_widget(self.applet)
		ev_box = gtk.EventBox()
		imgPrefs = gtk.Image()
		imgPrefs.set_from_stock (gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_BUTTON)
		
		self.btnPrefs = gtk.Button()
		self.btnPrefs.set_image(imgPrefs)
		
		imgEnter = gtk.Image()
		imgEnter.set_from_stock (gtk.STOCK_OK, gtk.ICON_SIZE_BUTTON)
		self.btnSend = gtk.Button()
		self.btnSend.set_image(imgEnter)		
		self.btnSend.connect ("clicked",self.on_btnSend_clicked)
		
		self.txtTweet = gtk.Entry()
		self.txtTweet.set_max_length(self.MaxChars)
		self.txtTweet.set_size_request(200,20)							# so netbook incompatible it might turn out to be
		self.txtTweet.connect("button_press_event",self.on_txtTweet_button_press_event)
		self.txtTweet.connect("button_release_event", self.on_txtTweet_button_release_event)
		self.txtTweet.connect("changed",self.on_txtTweet_changed)
		
		self.lblLeft = gtk.Label("140")
		
		main_hbox = gtk.HBox()
		main_hbox.pack_start(self.btnPrefs, False, False, 0)
		main_hbox.pack_start(self.txtTweet, False, False, 4)
		main_hbox.pack_start(self.lblLeft, False, False, 4)
		main_hbox.pack_start(self.btnSend, False, False, 4)
		
		ev_box.add(main_hbox)
		applet.add(ev_box)
		applet.show_all()

	
	def on_change_size (self):
		''' Todo: do something about your size '''
      
	
	def change_background(self, applet, type, color, pixmap):
		applet.set_style(None)
		applet.modify_style(gtk.RcStyle())
		if (type == gnomeapplet.COLOR_BACKGROUND):
				applet.modify_bg(gtk.STATE_NORMAL, color)
		elif (type == gnomeapplet.PIXMAP_BACKGROUND):
				applet.get_style().bg_pixmap[gtk.STATE_NORMAL] = pixmap


	def on_txtTweet_button_press_event(self, widget,event):
		''' give the focus to Applet so that Entry is accessible '''
		self.applet.request_focus(long(event.time))
		
		
	def on_txtTweet_button_release_event(self,widget,event):
		''' select old tweet for easy disappearance '''
		currentTweet = widget.get_text()
		
		if (currentTweet == self.oldTweet):
			widget.select_region(0,-1)
			widget.grab_focus()


	def on_txtTweet_changed(self,textbox):
		''' Update remaining characters '''
		tweet = textbox.get_text()
		
		if (len(tweet) == 0):
			self.btnSend.set_sensitive(False)
		else:
			self.btnSend.set_sensitive(True)
			
		self.lblLeft.set_text( str(self.MaxChars - len(tweet)) )


	def on_btnSend_clicked(self,button):
		''' validate, authenticate and post the tweet '''
		self.TweetThat()


	def TweetThat(self):
		''' tweets the content of txtTweet '''
		tweet = self.txtTweet.get_text()
		
		if (len(tweet.strip())==0):
			# a tweet made up of only spaces is not a tweet
			return
		
		self.api.SetCredentials (self.username, self.password)
		self.api.PostUpdate(tweet)
		
		self.oldTweet = tweet
		self.btnSend.set_sensitive(False)



def applet_factory(applet,oiid):
	TweetBar(applet)
	return True


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":  
	print "running in window"
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	main_window.set_title("Python Applet")
	main_window.connect("destroy", gtk.main_quit) 
	app = gnomeapplet.Applet()
	applet_factory(app, None)
	app.reparent(main_window)
	main_window.show_all()
	gtk.main()
	sys.exit()

gnomeapplet.bonobo_factory("OAFIID:GNOME_TweetBarApplet_Factory", 
                                gnomeapplet.Applet.__gtype__, 
                                "gtweetbar", "0", applet_factory)

