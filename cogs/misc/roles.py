from pprint import pprint

class Roles:
    def __init__(self):
        self._member = 1077860388114280498
        self._owner = 1077860355524546601
        self._admin = 1080415597063577610
        self._staff = 1077860360339591208
        self._driver = 1077860386986016819
        self._cars = {
            'Porsche': 1066758489206169623,
            'Mercedes': 1066758512530698314,
            'Chevrolet': 1066758534139740190,
            'Aston Martin': 1066758558651261038,
            'Ford': 1066758583158591591
        }
        self._leagues = {
            'D1': 930024457446232095,
            'D2': 930024502442729492,
            'D3': 940646795044851742
        }

    @property
    def member(self):
        return self._member

    @property
    def owner(self):
        return self._owner

    @property
    def admin(self):
        return self._admin

    @property
    def staff(self):
        return self._staff

    @property
    def driver(self):
        return self._driver

    @property
    def cars(self):
        return self._cars

    @property
    def leagues(self):
        return self._leagues







