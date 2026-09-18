def _require_positive(value, message):
    """Return value if it is a positive int/float (not a bool), else raise ValueError."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(message)
    return value


class Vehicle:
    kind = ""  # label shown before the make, e.g. "Electric"

    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    @property
    def status(self):
        return "rented" if self.is_rented else "available"

    def rent(self):
        if self.is_rented:
            raise RuntimeError(f"{self.plate} is already rented.")
        self.is_rented = True

    def return_vehicle(self):
        if not self.is_rented:
            raise RuntimeError(f"{self.plate} is not currently rented.")
        self.is_rented = False

    def details(self):
        """Extra info shown after the status. Subclasses override this."""
        return ""

    def __str__(self):
        name = f"{self.kind} {self.make} {self.model}".strip()
        text = f"{name} ({self.plate}) [{self.status}]"
        extra = self.details()
        return f"{text} - {extra}" if extra else text

    def __repr__(self):
        return f"{type(self).__name__}({self.make!r}, {self.model!r}, {self.plate!r})"


class ElectricCar(Vehicle):
    kind = "Electric"

    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = _require_positive(battery_kwh, "Battery size must be a positive number.")

    def details(self):
        return f"{self.battery_kwh} kWh battery"


class Motorbike(Vehicle):
    kind = "Motorbike"

    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = _require_positive(engine_cc, "Engine size must be a positive number.")

    def details(self):
        return f"{self.engine_cc} cc engine"


class Renter:
    def __init__(self, name, license_no):
        self.name = name
        self.license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must not be empty.")
        self._name = value.strip()

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        self._license_no = _require_positive(value, "License number must be a positive number.")
