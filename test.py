#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk

# make local copy of twitter api importable
import sys
sys.path.append('./python_twitter')
import twitter

class TweetBar(object):

	def __init__(self):
		''' setup everthing, load glade ui, set objects, defaults, etc '''
		
		self.builder=gtk.Builder()
		self.builder.add_from_file("ui/tweetbar.glade")
		self.builder.connect_signals( 
			{ 
			"on_mainwindow_destroy" : gtk.main_quit,
			"on_txtTweet_changed" : self.on_txtTweet_changed,
			"on_btnSend_clicked" : self.on_btnSend_clicked
			} 
		)
			
		self.window = self.builder.get_object("mainwindow")
		
		# Lets grab all controls before we reuse them elsewhere
		self.lblLeft = self.builder.get_object ("lblLeft")
		self.txtTweet = self.builder.get_object ("txtTweet")
		self.btnSend = self.builder.get_object ("btnSend")

		# init twitter API
		self.api = twitter.Api()
		self.MaxChars = 140

		self.window.show()

	def on_txtTweet_changed(self,textbox):
		''' Update remaining characters '''
		tweet = textbox.get_text()
		self.lblLeft.set_text( str(self.MaxChars - len(tweet)) )

	def on_btnSend_clicked(self,button):
		tweet = self.txtTweet.get_text()
		

if __name__=="__main__":
	app = TweetBar()
	gtk.main()
	
