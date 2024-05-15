class CustomList(list):
    def at(self, index):
        if 0 <= index < len(self):
            return self[index]
        else:
            return None


class CustomStr(str):
    def at(self, index):
        if 0 <= index < len(self):
            return self[index]
        else:
            return None
