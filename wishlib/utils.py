from os import path
import json


class JSONDict(dict):

    def __init__(self, fp, *args, **kwds):
        super(JSONDict, self).__init__(*args, **kwds)
        self.fp = fp
        if path.exists(fp):
            with open(self.fp) as fp:
                data = json.load(fp)
            self.update(data)

    def __setitem__(self, key, value):
        super(JSONDict, self).__setitem__(key, value)
        self.__updatejson__()

    def __delitem__(self, key):
        super(JSONDict, self).__delitem__(key)
        self.__updatejson__()

    def clear(self):
        super(JSONDict, self).clear()
        self.__updatejson__()

    def update(self, other):
        super(JSONDict, self).update(other)
        self.__updatejson__()

    def __updatejson__(self):
        with open(self.fp, "w") as fp:
            json.dump(self, fp, indent=4)
