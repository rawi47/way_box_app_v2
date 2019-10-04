from . import run,views
import  _thread, time,threading

def _initiate():
	print("############################ Starting main program #############################")
	try:
	    t1 = _thread.start_new_thread( views._save_status, () )
	except Exception as e:
	    print("Python exception : " + str(e))
