"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.calculation_done = 0
        destination = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        # Calculation of closest waypoint
        if (self.calculation_done == 0):
            current_closest_waypoint = landing_pad_locations[0]
            current_location_x = report.position.location_x
            current_location_y = report.position.location_y

            for location in landing_pad_locations:
                current_closest_distance = (current_closest_waypoint.location_x - current_location_x)**2 + (current_closest_waypoint.location_y - current_location_y)**2
                next_distance = (location.location_x - current_location_x)**2 + (location.location_y - current_location_y)**2

                if (next_distance < current_closest_distance):
                    current_closest_waypoint = location
   
            self.destination = current_closest_waypoint
            self.calculation_done = 1

        # Data for distance calculation between current position and waypoint
        current_location_x = report.position.location_x
        current_location_y = report.position.location_y
        waypoint_x = self.destination.location_x
        waypoint_y = self.destination.location_y

        pythagoras_x = (waypoint_x - current_location_x)**2
        pythagoras_y = (waypoint_y - current_location_y)**2
        pythagoras = pythagoras_x + pythagoras_y

        # Moving towards waypoint
        if (report.status == drone_status.DroneStatus.MOVING):
            if (pythagoras < (self.acceptance_radius)**2):
                command = commands.Command.create_halt_command()
        elif (report.status == drone_status.DroneStatus.HALTED):
            if (pythagoras < (self.acceptance_radius)**2):
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(waypoint_x - current_location_x, waypoint_y - current_location_y)

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
