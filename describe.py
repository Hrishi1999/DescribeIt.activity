# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""

import gi
import requests, base64

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf 
import urllib2


from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem


class DescribeItActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""
    
    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)
        self.set_canvas(box)

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()
        
        self.image = Gtk.Image()
        self.image.show()
        self.label = Gtk.Label()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        # label with the text, make the string translatable

        self.text = Gtk.Entry()

        self.text.show()
        #textbuffer = self.text.get_buffer()
        #textbuffer.set_text("hello")
        self.text.set_placeholder_text("URL")
        
        self.label.show()
        
        label1 = Gtk.Label()
        label1.show()
        label1.set_text("Image URL goes here")

        label2 = Gtk.Label()
        label2.show()
        label2.set_text("")
        
        button = Gtk.Button(_("Describe"))
        button.connect("clicked", self.on_open_clicked)
        box.show()
        box.add(label2)
        box.add(label1)
        box.add(self.text)
        button.show()
        box.add(button)
        box.add(self.image)
        box.add(self.label)

    def on_open_clicked(self, button):
                
       link = self.text.get_text()
       
       url = link
       response = urllib2.urlopen(url)
       fname = url.split("/")[-1]
       f = open(fname, "wb")
       f.write(response.read())
       f.close()
       response.close()
       self.image.set_from_pixbuf(Pixbuf.new_from_file(fname))
        
       headers = {
       # Request headers.
       'Content-Type': 'application/json',

       # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
       'Ocp-Apim-Subscription-Key': '2a697f81eabd47ca894ebdc80992b425',
       }

       params = {
       # Request parameters. All of them are optional.
       'visualFeatures': 'Description',
       'details': 'Celebrities',
       'language': 'en',
       }

       # Replace the three dots below with the URL of a JPEG image of a celebrity.
       body = {'url': link
       }
       
       try:
           # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
           #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
           #   URL below with "westus".
           response = requests.post(url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                                    headers = headers,
                                    params = params,
                                    json = body)
           data = response.json()
           #rint(data['description']['captions'][0]['text'])
           str1 = str(data['description']['captions'][0]['text'])
           self.label.set_text(str1)

       except Exception as e:
           print("Err")
       
       self.label.set_text(str1)

    
