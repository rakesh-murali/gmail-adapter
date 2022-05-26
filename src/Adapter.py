class Adapter:
    _initialised = False

    def __init__(self, minion, **adapted_methods):
        self.minion = minion

        for key, value in adapted_methods.items():
            func = getattr(self.minion, value)
            self.__setattr__(key, func)

        self._initialised = True

    def __getattr__(self, attr):
        """
          Attributes not in Adapter are delegated to the minion
        """
        return getattr(self.minion, attr)

    def __setattr__(self, key, value):
        """
          Set attributes normally during initialisation
        """
        if not self._initialised:
            super().__setattr__(key, value)
        else:
            """
              Set attributes on minion after initialisation
            """
            setattr(self.minion, key, value)