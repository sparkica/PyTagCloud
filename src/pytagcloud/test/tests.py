# -*- coding: utf-8 -*-
from copy import copy
from pytagcloud import create_tag_image, create_html_data, make_tags, LAYOUT_MIX, \
    LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
import os
import time
import unittest

class Test(unittest.TestCase):
    """
    Generate tag clouds and save them to <YOURHOME>/pytagclouds/
    """
    
    def setUp(self):
        home_folder = os.getenv('USERPROFILE') or os.getenv('HOME')
        self.test_images = os.path.join(home_folder, 'pytagclouds')
        self.hound = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pg2852.txt'), 'r')
        
        if not os.path.exists(self.test_images):
            os.mkdir(self.test_images )            
            
    def tearDown(self):
        self.hound.close()
        
    def test_tag_counter(self):
        tag_list = get_tag_counts(self.hound.read())[:50]     
        self.assertTrue(('sir', 350) in tag_list)

    def test_make_tags(self):
        mtags = make_tags(get_tag_counts(self.hound.read())[:60])
        found = False
        for tag in mtags:
            if tag['tag'] == 'sir' and tag['size'] == 40:
                found = True
                break
            
        self.assertTrue(found)

    def test_create_tag_image(self):
        start = time.time()
        tags = make_tags(get_tag_counts(self.hound.read())[:30])
        for layout in LAYOUTS:
            create_tag_image(tags, os.path.join(self.test_images, 'cloud_%s.png' % layout), size=(600, 500), background=(255, 255, 255, 255), layout=layout, crop=True, fontname='Lobster.ttf', fontzoom=3)
        print "Duration: %d sec" % (time.time() - start)

    def test_create_tag_image_rect(self):
        start = time.time()
        create_tag_image(make_tags(get_tag_counts(self.hound.read())[:30]), os.path.join(self.test_images, 'cloud_rect.png'), size=(300, 400), background=(255, 255, 255, 255), layout=LAYOUT_HORIZONTAL, crop=False, rectangular=True, fontname='Lobster.ttf', fontzoom=2)
        print "Duration: %d sec" % (time.time() - start)

    def test_create_html_data(self):
        """
        HTML code sample
        """
        data = create_html_data(make_tags(get_tag_counts(self.hound.read())[:30]), size=(600, 400), fontname='Lobster.ttf', fontzoom=3)
        print '\nCSS\n'
        for style in data['css']:
            print style

        print '\nHTML\n'
        for link in data['links']:
            print '<a class="tag %(cls)s" href="#" style="top: %(top)dpx; left: %(left)dpx; font-size: %(size)dpx;">%(tag)s</a>' % link

if __name__ == "__main__":
    unittest.main()