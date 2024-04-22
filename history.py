class HistoryHandler:
    def __init__(self):
        self.last_entry = 0
        self.history_complete = {}
        self.temp_single_filter = {}
        self.temp_ids = []

    def addToHistory(self, text: str, multy_history: bool, once: str):
        self.last_entry += 1
        self.history_complete[self.last_entry] = text

        if once:
            self.history_complete.pop(self.temp_single_filter.get(once, -1), None)
            self.temp_single_filter[once] = self.last_entry
        elif multy_history:
            self.temp_ids.append(self.last_entry)
        else:
            for id in self.temp_ids:
                self.history_complete.pop(id, None)
            self.temp_ids = []

    def viewHistory(self):
        return "\n".join(self.history_complete.values())
