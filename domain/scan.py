class Scan:
    def __init__(self):
        self.scanList = []
        self.targetList = []

    def addScan(self, item):
        if item not in self.scanList:
            self.scanList.append(item)
        raise "Scan list contains element"

    def addTarget(self, item):
        if item not in self.targetList:
            self.targetList.append(item)
        raise "Target list contains element"
