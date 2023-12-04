from enum import Enum


class District(str, Enum):
    """Saint Petersburg districts."""

    admiralteysky = "admiralteysky"
    vasileostrovsky = "vasileostrovsky"
    vyborg = "vyborg"
    kalininsky = "kalininsky"
    kirovsky = "kirovsky"
    kolpinsky = "kolpinsky"
    krasnogvardeisky = "krasnogvardeisky"
    krasnoselsky = "krasnoselsky"
    kronstadt = "kronstadt"
    kurortny = "kurortny"
    moscow = "moscow"
    nevsky = "nevsky"
    petrogradsky = "petrogradsky"
    petrodvortsovy = "petrodvortsovy"
    primorsky = "primorsky"
    pushkinsky = "pushkinsky"
    frunzensky = "frunzensky"
    central = "central"


class Cuisine(str, Enum):
    """Supported cuisines."""

    russia = "russia"
    china = "china"
    japan = "japan"
    georgia = "georgia"
    italy = "italy"
    korea = "korea"
    mexico = "mexico"
    uzbekistan = "uzbekistan"


class CafeType(str, Enum):
    """Supported cafe types."""

    restaurant = "restaurant"
    cafe = "cafe"
    canteen = "canteen"
