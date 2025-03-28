from typing import Protocol


class ILightingSystem(Protocol):

    def turn_on() -> None: ...
    def turn_off() -> None: ...


class IClimateControl(Protocol):

    def set_temperature(temp: float) -> None: ...
    def turn_on() -> None: ...
    def turn_off() -> None: ...


class ISecuritySystem(Protocol):
    def arm() -> None: ...
    def disarm() -> None: ...


class Facade:
    def __init__(
        self,
        lighting: ILightingSystem,
        climate: IClimateControl,
        security: ISecuritySystem,
    ):
        self.lighting = lighting
        self.climate = climate
        self.security = security

    def turn_off_light(self):
        self.lighting.turn_off()

    def turn_on_light(self):
        self.lighting.turn_on()

    def arm_activate(self):
        self.security.arm()

    def arm_disable(self):
        self.security.disarm()


class LightingSystem:
    def turn_on():
        print("вкл свет")

    def turn_off():
        print("выкл свет")


class ClimateControl:

    def set_temperature(temp: float) -> None:
        print(f"температура сейчас {temp}")

    def turn_on() -> None:
        print("вкл климат")

    def turn_off() -> None:
        print("выкл климат")


class SecuritySystem:
    def arm() -> None:
        print("вкл защиту")

    def disarm() -> None:
        print("выкл защиту")


lighting_system = LightingSystem()
climate_control = ClimateControl()
security_system = SecuritySystem()

control_panel = Facade(
    lighting=lighting_system,
    climate=climate_control,
    security=security_system,
)
