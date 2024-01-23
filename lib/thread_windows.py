import lib.thread_abtractions
class Loader(lib.thread_abtractions.BaseThreading):
    def start(self, name, target, args):
        import threading
        th = threading.Thread(target=target,args=args)
        th.name=name
        th.start()
        return th
    def join(self, list_of_thread):
        for x in  list_of_thread:
            x.join()