


from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.classes import ClassSymbolGatherer
from blast_radius.parsers.imports import ImportGatherer
from blast_radius.parsers.standalone_functions import StandaloneFunctionGatherer


class EntireFileSymbolGatherer(BaseNodeVisitor):

    imports: list[ImportGatherer] # TODO rename ImportSymbolGatherer
    classes: list[ClassSymbolGatherer]
    standalone_functions: list[StandaloneFunctionGatherer]


