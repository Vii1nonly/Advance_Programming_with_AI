from rental import Vehicle, ElectricCar, Motorbike, Renter


def show_section(title):
    print(f"\n--- {title} ---")


def show_fleet(fleet):
    for number, vehicle in enumerate(fleet, start=1):
        print(f"{number}. {vehicle}")


def check_out(renter, vehicle):
    vehicle.rent()
    renter.rented.append(vehicle)
    print(f"{renter.name} checked out -> {vehicle}")


def check_in(renter, vehicle):
    vehicle.return_vehicle()
    if vehicle in renter.rented:
        renter.rented.remove(vehicle)
    print(f"{renter.name} checked in  -> {vehicle}")


def show_renter(renter):
    print(f"Renter      : {renter.name}")
    print(f"Licence no. : {renter.license_no}")
    print(f"Currently has {len(renter.rented)} vehicle(s): {renter.rented}")


def expect_error(description, action):
    """Run an action that should fail, and report whether validation stopped it."""
    try:
        action()
    except ValueError as err:
        print(f"[OK]   {description}: {err}")
    else:
        print(f"[FAIL] {description}: no error was raised")


def run_validation_checks(renter):
    checks = [
        ("Empty name on create", lambda: Renter("", 55501)),
        ("Zero licence on create", lambda: Renter("Mina", 0)),
        ("Blank name on update", lambda: setattr(renter, "name", "")),
        ("Negative licence on update", lambda: setattr(renter, "license_no", -7)),
    ]
    for description, action in checks:
        expect_error(description, action)


def main():
    fleet = [
        Vehicle("Mazda", "2", "7CX412"),
        ElectricCar("BYD", "Dolphin", "8EV903", 45),
        Motorbike("Suzuki", "Burgman", "9MB275", 200),
    ]
    renter = Renter("Mina", 55501)

    show_section("Fleet")
    show_fleet(fleet)

    show_section("Checkout / Check-in")
    first_car = fleet[0]
    check_out(renter, first_car)
    check_in(renter, first_car)

    show_section("Renter Details")
    show_renter(renter)

    show_section("Validation")
    run_validation_checks(renter)

    show_section("Polymorphism: same call, different classes")
    for vehicle in fleet:
        print(f"{type(vehicle).__name__:<12} {vehicle}")


if __name__ == "__main__":
    main()
