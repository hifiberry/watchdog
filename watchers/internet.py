'''
Copyright (c) 2020 Modul 9/HiFiBerry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import time
import requests
import logging

from watchers.watcher import Watcher

class Internet(Watcher):


    def __init__(self, params={}):
        super().__init__()
        self.name = "internet"
        self.ok = True
        try:
            self.test_interval = int(params["test_interval"])
        except:
            self.test_interval=300 
                
        try:
            self.max_fails = int(params["max_fails"])
        except:
            self.max_fails = 3
            
        try:
            self.test_servers = params["servers"].split(",")
        except:
            self.test_servers=["www.google.com","www.wikipedia.org","www.facebook.com"]
            
        logging.info("internet watcher every %s seconds, max %s fails, watching %s",
                     self.test_interval, self.max_fails, self.test_servers)
        
        self.fails = 0

    
    def is_ok(self):
        return self.ok
        
    def run(self):
        
        while (True):
            ok = False
            for s in self.test_servers:
                url = "https://{}/".format(s)
                try:
                    requests.get(url, timeout=10)
                    ok = True
                    break
                except Exception as e:
                    logging.info("error retrieving %s: %s", url, e)
                    pass
                
            if ok:
                self.fails = 0
                self.ok = True
            else:
                self.fails += 1
                logging.info("fails: %s (max=%s)",self.fails,self.max_fails)
                if self.fails >= self.max_fails:
                    self.ok = False
                    logging.debug("self.ok: %s",self.ok)
            
            time.sleep(self.test_interval)
