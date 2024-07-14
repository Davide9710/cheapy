class StartCommand:
    def execute(self, user):
        user.state = 'initial'
        return "Welcome! How can I help you today?"