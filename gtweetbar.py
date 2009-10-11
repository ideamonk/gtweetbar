#!/usr/bin/env python
## gtweetbar.py -- a GNOME Applet that lets you tweet on the fly
 
# ======================================================================
# Copyright (C) 2009 Abhishek Mishra <ideamonk@gmail.com>
# Time-stamp: Sun Oct 04 12:11:57 IST 2009
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

INSTALL_PATH = "/usr/share/gtweetbar"

import pygtk
pygtk.require("2.0")
import gtk
import gnomeapplet
import gconf

# make local copy of twitter api importable
import sys
sys.path.append(INSTALL_PATH + '/python_twitter')
import twitter


class TweetBar(object):
	oldTweet = ""
	MaxChars = 140
	
	## Events ==================================================================
	def on_txtTweet_keypress_event(self,entry,event):
		if (gtk.gdk.keyval_name(event.keyval) == 'Return'):
			self.TweetThat()
			self.txtTweet.select_region(0,-1)			# select the sent tweet for easy removal
	
	def on_change_size (self):
		''' Todo: do something about your size '''
    
    def on_change_background(self, applet, type, color, pixmap):
		applet.set_style(None)
		applet.modify_style(gtk.RcStyle())
		if (type == gnomeapplet.COLOR_BACKGROUND):
				applet.modify_bg(gtk.STATE_NORMAL, color)
		elif (type == gnomeapplet.PIXMAP_BACKGROUND):
				applet.get_style().bg_pixmap[gtk.STATE_NORMAL] = pixmap
 	
 	def on_btnPrefs_clicked(self,button):
		self.get_credentials("GTweetBar Preferences")
	
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
		
	def on_config_event(self, gconf_client, *args, **kwargs):
		''' refresh credentials on change '''
		self.username = self.gconf_client.get_string("/apps/gtweetbar/auth/username")
		self.password = self.gconf_client.get_string("/apps/gtweetbar/auth/password")
		
 	## Methods =================================================================
	def get_credentials(self,message):
		''' shows a preference box to let user change credentials '''
		dia = gtk.Dialog('Gnome TweetBar',
				          self.applet.get_toplevel(),  #the toplevel wgt of your app
				          gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
				          (gtk.STOCK_OK, gtk.RESPONSE_OK))
				          
		txtUsername = gtk.Entry()
		txtPassword = gtk.Entry()
		txtPassword.set_visibility(False)				# a password box :)
		lblUsername = gtk.Label ("Username : ")
		lblPassword = gtk.Label ("Password : ")
			
		# load pre-stored credentials into the text boxes
		txtUsername.set_text (self.username)
		txtPassword.set_text (self.password)

		hbox1 = gtk.HBox()
		hbox2 = gtk.HBox()

		# packup everything into a vbox
		'''
								+-vbox---------
								|  [hbox1]    |
								|  [hbox2]    |
								|        [ok] |
								===============
		'''
		hbox1.pack_start(lblUsername,False,False,2)
		hbox1.pack_start(txtUsername,False,False,2)
		hbox2.pack_start(lblPassword,False,False,2)
		hbox2.pack_start(txtPassword,False,False,6)	# this padding is dependent on theme/etc
		dia.vbox.pack_start(gtk.Label(message),False,False,10)
		dia.vbox.pack_start(hbox1)
		dia.vbox.pack_start(hbox2)
		
		dia.show_all()
		result = dia.run()
		
		if result == gtk.RESPONSE_OK:
			# lets verify
			username = txtUsername.get_text()
			password = txtPassword.get_text()
			if (username=="" or password == "" or len(password)<=4):
				# something wen't wrong
				dia.destroy()
				self.get_credentials("Hey enter something real!")
				return
			else:
				# okay so lets store this credential
				self.username = username
				self.password = password
				self.update_settings()
				
		dia.destroy()

	def update_settings(self):
		''' stores the current credentials back to gconf '''
		self.gconf_client.set_string("/apps/gtweetbar/auth/username",self.username)
		self.gconf_client.set_string("/apps/gtweetbar/auth/password",self.password)
		
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
	
	
	## Big Bang -- where it all began :P =======================================	
	def __init__(self,applet):
		self.api = twitter.Api()
		self.gconf_client = gconf.client_get_default()
		#self.gconf_client.notify_add("/apps/gtweetbar/auth", self.config_event)
		
		# lets save a reference for future use
		self.applet = applet
		self.applet.connect("change-size", self.on_change_size)
		self.applet.connect("change-background", self.on_change_background)
    
		## interface build up
		self.applet.set_background_widget(self.applet)
		ev_box = gtk.EventBox()
		
		# preference button
		imgPrefs = gtk.Image()
		imgPrefs.set_from_stock (gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_BUTTON)
		self.btnPrefs = gtk.Button()
		self.btnPrefs.set_image(imgPrefs)
		self.btnPrefs.connect("clicked",self.on_btnPrefs_clicked)
		
		# send button
		imgEnter = gtk.Image()
		imgEnter.set_from_stock (gtk.STOCK_OK, gtk.ICON_SIZE_BUTTON)
		self.btnSend = gtk.Button()
		self.btnSend.set_image(imgEnter)		
		self.btnSend.connect ("clicked",self.on_btnSend_clicked)
		
		# Entry box for tweet
		self.txtTweet = gtk.Entry()
		self.txtTweet.set_max_length(self.MaxChars)
		# it might turn out to be netbook incompatible
		self.txtTweet.set_size_request(200,20)
		self.txtTweet.connect("button_press_event",self.on_txtTweet_button_press_event)
		self.txtTweet.connect("button_release_event", self.on_txtTweet_button_release_event)
		self.txtTweet.connect("changed",self.on_txtTweet_changed)
		self.txtTweet.connect("key-press-event",self.on_txtTweet_keypress_event)
		
		self.lblLeft = gtk.Label("140")
		
		# packup everything into their respective places
		main_hbox = gtk.HBox()
		main_hbox.pack_start(self.btnPrefs, False, False, 0)
		main_hbox.pack_start(self.txtTweet, False, False, 4)
		main_hbox.pack_start(self.lblLeft, False, False, 4)
		main_hbox.pack_start(self.btnSend, False, False, 0)
		
		# lets load the config before we show up the ui
		self.username = self.gconf_client.get_string("/apps/gtweetbar/auth/username")
		self.password = self.gconf_client.get_string("/apps/gtweetbar/auth/password")

		if (self.username == None or self.username == ""):
			# ask username and password from user for first run
			self.get_credentials("You need to add your twitter account to gtweetbar.")
						
		ev_box.add(main_hbox)
		applet.add(ev_box)
		applet.show_all()
		

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

