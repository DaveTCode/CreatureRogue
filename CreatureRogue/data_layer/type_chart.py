from typing import Mapping

from CreatureRogue.data_layer.type import Type


class TypeChart:
    def __init__(self, chart: Mapping[Type, Mapping[Type, int]]):
        self.chart = chart

    def damage_modifier(self, attacking_type: Type, defending_type: Type) -> int:
        """
            The type chart hold information on how attacks of all types affect
            creatures of all types. This function allows us to query that
            information.

            :param defending_type: A species/move type.
            :param attacking_type: A species/move type.

            :return: The integer factor which corresponds to the percentage
            damage adjustment (so 100 is default).
        """
        if attacking_type in self.chart and defending_type in self.chart[attacking_type]:
            return self.chart[attacking_type][defending_type]
        else:
            return 100

    def __str__(self):
        type_chart_str = ""

        for attacking_type in self.chart:
            type_chart_str = str(attacking_type) + " - "

            type_chart_str += ",".join(["({0}:{1}), ".format(defending_type, self.chart[attacking_type][defending_type]) for defending_type in self.chart[attacking_type]]) + "\n"

        return type_chart_str
