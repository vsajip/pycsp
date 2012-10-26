"""
Constants

Copyright (c) 2009 John Markus Bjoerndalen <jmb@cs.uit.no>,
      Brian Vinter <vinter@diku.dk>, Rune M. Friborg <runef@diku.dk>.
See LICENSE.txt for licensing details (MIT License). 
"""
import threading
try:
    import multiprocessing
except:
    pass

import platform
USE_CTYPES=1

if platform.python_implementation()=='PyPy':
    USE_CTYPES=0


ENVVAL_PORT = 'PYCSP_PORT'

# Setup
PICKLE_PROTOCOL= 2
ENABLE_CACHE = 1

# Operation type
READ, WRITE = range(2)

# Constants used for both ChannelReq results and ReqStatus states.
READY, FAIL, SUCCESS, POISON, RETIRE = range(5)


def getThreadAndName():
    thread = None
    name = None

    # Get thread from threading first, since if thread is set, then
    # we do not have to look up multiprocessing
    try:
        # compatible with Python 2.6+
        thread = threading.current_thread()
    except AttributeError:
        # compatible with Python 2.5- 
        thread = threading.currentThread()
    
    name = thread.getName()

    if name == 'MainThread':
        # This might be a multiprocess, thus multiprocessing must be checked
        p = None
        parent_pid = None
        try:
            p = multiprocessing.current_process()
            parent_pid = p._parent_pid
        except:
            pass

        if not parent_pid:
            # This is the main process!
            try:
                if thread.id:
                    name = thread.id
            except AttributeError:
                # Not initilialised yet
                # Will be initialised  by pycsp.process.init()
                pass
        else:
            # p is a MultiProcess
            thread = p
            name = p.name

    return (thread, name)