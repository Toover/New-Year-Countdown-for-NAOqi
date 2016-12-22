import qi

class NewYearCountdownService:

    def ping(self):
        pass

if __name__ == '__main__':
    app = qi.Application()
    app.start()
    service = NewYearCountdownService()
    app.session.registerService('NewYearCountdown', service)
    app.run()
