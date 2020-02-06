'''
Copyright (c) 2018 Modul 9/HiFiBerry

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

import logging
import sys
import time
import configparser

class Watchdog():
    
    def __init__(self):
        self.watchers = []
        pass
    
    
    def add_watcher(self, watcher):
        self.watchers.append(watcher) 
        
    def has_failed(self):
        '''
        Checks the state of all watchers and resets it. This should not be called more often than once
        every 5 seconds as it will reset the state of the watchers.
        '''
        failed = []
        for watcher in self.watchers:
            if not(watcher.is_ok()):
                failed.append(watcher)
                
        return failed
    
    def run(self):
        while True:
            failed = self.has_failed()
            if len(failed) == 0:
                logging.debug("ok, updating watchdog")
                f = open("/dev/watchdog", "w")
                f.write("watchdog ok")
                f.close()
            else:
                logging.debug("failed watchers: %s", failed)
            time.sleep(7)
            
            
def create_watcher(classname, params = {}):
    import importlib
    module_name, class_name = classname.rsplit(".", 1)
    MyClass = getattr(importlib.import_module(module_name), class_name)
    
    watcher = MyClass(params)

    return watcher
            
            
def read_config(watchdog):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option

    config.read("/etc/watchdog.conf")

    # Additional controller modules
    for section in config.sections():
        if section.startswith("watcher:"):
            try:
                [_,classname] = section.split(":",1)
                params = config[section]
                watcher = create_watcher(classname, params)
                watcher.start()
                watchdog.add_watcher(watcher)
                logging.info("started watcher %s", watcher)
            except Exception as e:
                logging.error("Exception during rotary control initialization")
                logging.exception(e)


if __name__ == '__main__':

    if "-v" in sys.argv:
        logging.basicConfig(format='%(levelname)s: %(name)s - %(message)s',
                            level=logging.DEBUG)
        logging.debug("enabled verbose logging")
    else:
        logging.basicConfig(format='%(levelname)s: %(name)s - %(message)s',
                            level=logging.INFO)


    watchdog = Watchdog()
    read_config(watchdog) 
    
    # Run idle loop
    logging.info("starting watchdog main loop")
    watchdog.run()