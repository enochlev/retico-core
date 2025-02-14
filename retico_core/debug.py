"""
Debug Module
============

This file contains general debug modules that can be used to output information from any
incremental unit.
"""


from retico_core import abstract


class DebugModule(abstract.AbstractConsumingModule):
    """A debug module that prints the IUs that are coming in."""

    @staticmethod
    def name():
        return "Debug Module"

    @staticmethod
    def description():
        return "A consuming module that displays IU infos in the console."

    @staticmethod
    def input_ius():
        return [abstract.IncrementalUnit]

    def __init__(self, print_payload_only=False):
        super().__init__()
        self.print_payload_only = print_payload_only

    def process_update(self, update_message):
        if self.print_payload_only:
            for iu, ut in update_message:
                print(ut, iu.payload)
        else:
            print(f"Debug: Update Message ({len(update_message)})")
            for i, (iu, ut) in enumerate(update_message):
                print(f"{i}: {iu} (UpdateType: {ut})")
                print("  PreviousIU:", iu.previous_iu)
                print("  GroundedInIU:", iu.grounded_in)
                print("  Age:", iu.age())
            print(f"End of Debug Message")


class CallbackModule(abstract.AbstractConsumingModule):
    """A debug module that returns the incoming update messages into a callback
    function."""

    @staticmethod
    def name():
        return "Callback Debug Module"

    @staticmethod
    def description():
        return (
            "A consuming module that calls a callback function whenever an"
            "update message arrives."
        )

    @staticmethod
    def input_ius():
        return [abstract.IncrementalUnit]

    def __init__(self, callback, **kwargs):
        """Initializes the module with a callback function that has to take one argument
        that contains the update message whenever it arrives.
        """
        super().__init__(**kwargs)
        self.callback = callback

    def process_update(self, update_message):
        self.callback(update_message)
