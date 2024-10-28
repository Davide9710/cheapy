class InitialState:
    def handle(self, user, message):
        return "Hello! What would you like to do?", "awaiting_input"