class AwaitingInputState:
    def handle(self, user, message):
        return f"You said: {message}", "awaiting_input" 