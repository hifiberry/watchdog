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
import unittest
from time import sleep

from watchers.internet import Internet

def create_watcher(params):
    return Internet(params)

class InternetTest(unittest.TestCase):

    def testUnknown(self):
        watcher = create_watcher({
            "test_interval": 1,
            "max_fails": 1,
            "servers": "xxx.yyy.zzz"
        })
        assert watcher.is_ok()
        watcher.start()
        sleep(2)
        assert watcher.is_ok() == False
        watcher.stop()
        sleep(2)
        
    def testOK(self):
        watcher = create_watcher({
            "test_interval": 2,
            "max_fails": 2,
            "test_servers": "www.google.com"
        })
        assert watcher.is_ok()
        watcher.start()
        sleep(5)
        assert watcher.is_ok()
        sleep(5)
        assert watcher.is_ok()
        watcher.stop()
        sleep(3)

if __name__ == "__main__":
    unittest.main()