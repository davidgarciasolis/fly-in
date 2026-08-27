"""Console rendering for simulation movements."""

from movement import Movement


class Renderer:
    """Format and print movements generated during a simulation."""

    def __init__(self, use_color: bool = False) -> None:
        """Set whether ANSI colors should be used in the output."""
        self.use_color: bool = use_color
        self.color_codes: dict[str, str] = {
                "black": "30", "red": "31", "green": "32", "yellow": "33",
                "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
                "gray": "90", "orange": "33", "purple": "35", "brown": "33",
                "lime": "92", "gold": "93", "maroon": "31", "darkred": "31",
                "crimson": "31", "violet": "35",
            }

    def print_movements(self, movements: list[Movement]) -> None:
        """Print the movements performed during one turn."""
        ordered_movements = sorted(movements)
        texts = [
            self.build_movement(movement) for movement in ordered_movements
        ]
        print(" ".join(texts))

    def build_movement(self, movement: Movement) -> str:
        """Build the output text representing one movement."""
        drone = movement.get_drone()
        hub = movement.get_hub()
        connection = movement.get_connection()
        identifier = drone.get_identifier()

        if hub is not None:
            text = f"D{identifier}-{hub.name}"
            return self.colorize(text, hub.color)
        if connection is not None:
            origin = connection.origin.name
            destination = connection.destination.name
            return f"D{identifier}-{origin}-{destination}"
        return ""

    def colorize(self, text: str, color: str | None) -> str:
        """Return text wrapped in an ANSI color code when enabled."""
        if not self.use_color or color is None:
            return text
        code = self.color_codes.get(color.lower())
        if code is None:
            return text
        return f"\033[{code}m{text}\033[0m"
