from pprint import pprint

class Roles:
    def __init__(self):
        self._member = 1077860388114280498
        self._owner = 1077860355524546601
        self._admin = 1080415597063577610
        self._staff = 1077860360339591208
        self._driver = 1077860386986016819
        self._cars = {
            'Porsche': 1088907881220419696,
            'Mercedes': 1088907864413851658,
            'Ferrari': 1088907911855603783,
            'Aston Martin': 1088907897724997654,
            'Ford': 1088907842565709854
        }
        self._leagues = {
            'D1': 1087485153732989102,
            'D2': 1087485196238073936,
            'D3': 1087485236671164416
        }
        self._quali = {
            'Q-1': 1087490608211439816,
            'Q-2': 1087490630185398314,
            'Q-3': 1087490650313850880,
            'Q-4': 1087490659855892520,
            'Q-5': 1087490672312995850,
            'Q-6': 1087490684434526258,
            'Q-7': 1087490694609903759,
            'Q-8': 1087490706634985592,
            'Q-9': 1097251692896075887
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

    @property
    def quali(self):
        return self._quali







