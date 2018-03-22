import copy
import itertools
<<<<<<< HEAD
import xml
from xml.dom import minidom
import xml.etree.ElementTree as ET

import numpy

from urh.cythonext.signalFunctions import Symbol
=======

import numpy

>>>>>>> b1ae517... Inital Commit
from urh.models.ProtocolTreeItem import ProtocolTreeItem
from urh.signalprocessing.Modulator import Modulator
from urh.signalprocessing.ProtocoLabel import ProtocolLabel
from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
<<<<<<< HEAD
from urh.signalprocessing.Message import Message
from urh.signalprocessing.ProtocolGroup import ProtocolGroup
from urh.signalprocessing.encoder import Encoder
from urh.util.Formatter import Formatter
from urh.util.Logger import logger
from enum import Enum

class FuzzMode(Enum):
    successive = 0
    concurrent = 1
    exhaustive = 2
=======
from urh.signalprocessing.ProtocolBlock import ProtocolBlock
from urh.signalprocessing.ProtocolGroup import ProtocolGroup
>>>>>>> b1ae517... Inital Commit

class ProtocolAnalyzerContainer(ProtocolAnalyzer):
    """
    A container to manage several ProtocolAnalyzers.
    This class is used by the generator to manage distinct protocols
    """

<<<<<<< HEAD
    def __init__(self, modulators):
        """

        :type modulators: list of Modulator
        """
        super().__init__(None)
        self.modulators = modulators

        self.fuzz_pause = 10000
=======
    def __init__(self, modulators, decoders):
        """

        :type modulators: list of Modulator
        :type decoders: list of encoding
        """
        super().__init__(None)
        self.modulators = modulators
        self.decoders = decoders

        self.fuzz_pause = 10000
        self.created_fuz_blocks = []
>>>>>>> b1ae517... Inital Commit

        self.__group = ProtocolGroup("GeneratorGroup")
        self.__group.add_protocol_item(ProtocolTreeItem(self, None)) # Warning: parent is None

    @property
    def protocol_labels(self):
<<<<<<< HEAD
        result = list(set(lbl for msg in self.messages for lbl in msg.message_type))
        result.sort()
        return result

    @property
    def multiple_fuzz_labels_per_message(self):
        return any(len(msg.active_fuzzing_labels) > 1 for msg in self.messages)

    def insert_protocol_analyzer(self, index: int, proto_analyzer: ProtocolAnalyzer):

        messages = [Message(plain_bits=copy.copy(msg.decoded_bits), pause=msg.pause,
                            message_type=copy.deepcopy(msg.message_type),
                            rssi=msg.rssi, modulator_indx=0, decoder=msg.decoder, bit_len=msg.bit_len, participant=msg.participant)
                  for msg in proto_analyzer.messages if msg]

        self.messages[index:0] = messages
        self.used_symbols |= proto_analyzer.used_symbols

        if len(self.pauses) > 0:
            self.fuzz_pause = self.pauses[0]

    def duplicate_line(self, row: int):
        try:
            self.messages.insert(row + 1, copy.deepcopy(self.messages[row]))
            self.qt_signals.line_duplicated.emit()
        except Exception as e:
            logger.error("Duplicating line ", str(e))

    def fuzz(self, mode: FuzzMode, default_pause=None):
        result = []
        appd_result = result.append

        for i, msg in enumerate(self.messages):
            labels = msg.active_fuzzing_labels
            appd_result(msg)

            if mode == FuzzMode.successive:
                combinations = [[(l.start, l.end, fuzz_val)] for l in labels for fuzz_val in l.fuzz_values[1:]]
            elif mode == FuzzMode.concurrent:
                nval = numpy.max([len(l.fuzz_values) for l in labels]) if labels else 0
                f = lambda index, label: index if index < len(label.fuzz_values) else 0
                combinations = [[(l.start, l.end, l.fuzz_values[f(j, l)]) for l in labels] for j in range(1, nval)]
            elif mode == FuzzMode.exhaustive:
                pool = [[(l.start, l.end, fv) for fv in l.fuzz_values[1:]] for l in labels]
                combinations = itertools.product(*pool) if labels else []
            else:
                raise ValueError("Unknown fuzz mode")

            for combination in combinations:
                cpy_bits = msg.plain_bits[:]
                for start, end, fuz_val in combination:
                    cpy_bits[start:end] = [True if bit == "1" else False for bit in fuz_val]

                pause = default_pause if default_pause is not None else msg.pause
                fuz_msg = Message(plain_bits=cpy_bits, pause=pause,
                                  rssi=msg.rssi, message_type=msg.message_type.copy_for_fuzzing(),
                                  modulator_indx=msg.modulator_indx,
                                  decoder=msg.decoder, fuzz_created=True)
                appd_result(fuz_msg)

        self.messages = result
        """:type: list of Message """

    def fuzz_successive(self, default_pause=None):
=======
        return self.__group.labels

    @property
    def num_blocks_successive_fuzzing(self):
        result = self.num_blocks
        for i in range(self.num_blocks):
            result += sum([len(l.fuzz_values) for l in self.protocol_labels if l.refblock == i and l.active_fuzzing])

        return result

    @property
    def num_blocks_concurrent_fuzzing(self):
        result = self.num_blocks
        for i in range(self.num_blocks):
            vals = [len(l.fuzz_values) for l in self.protocol_labels if l.refblock == i and l.active_fuzzing]
            if len(vals) > 0:
                result += numpy.max(vals)

        return result

    @property
    def num_blocks_exhaustive_fuzzing(self):
        result = self.num_blocks
        for i in range(self.num_blocks):
            vals = [len(l.fuzz_values) for l in self.protocol_labels if l.refblock == i and l.active_fuzzing]
            if len(vals) > 0:
                result += numpy.product(vals)

        return result

    @property
    def active_fuzzing_labels(self):
        return [p for p in self.protocol_labels if p.active_fuzzing]

    @property
    def has_fuzz_labels_with_same_block(self):
        act_labels = self.active_fuzzing_labels
        return any(p1.refblock == p2.refblock
                   for p1 in act_labels for p2 in act_labels if p1 != p2)

    def insert_protocol_analyzer(self, index: int, proto_analyzer: ProtocolAnalyzer):

        blocks = [ProtocolBlock(copy.copy(block.decoded_bits), block.pause,
                                self.bit_alignment_positions, block.rssi, 0, block.decoder, bit_len=block.bit_len,
                                exclude_from_decoding_labels=copy.copy(block.exclude_from_decoding_labels))
                  for block in proto_analyzer.blocks if block]

        self.blocks[index:0] = blocks
        self.used_symbols |= proto_analyzer.used_symbols

        proto_labels = [copy.deepcopy(lbl) for lbl in proto_analyzer.protocol_labels]

        for l in proto_labels:
            l.refblock += index

        for l in self.protocol_labels:
            if l.refblock > index:
                l.refblock += proto_analyzer.num_blocks

        for p in proto_labels:
            self.__group.add_label(p)

        for block in self.blocks:
            block.fuzz_labels[index:0] = [p for p in proto_labels if p not in block.fuzz_labels]

        if len(self.pauses) > 0:
            self.fuzz_pause = self.pauses[0]

        self.refresh_protolabel_blocks()

    def duplicate_line(self, row: int):
        self.blocks.insert(row + 1, copy.deepcopy(self.blocks[row]))
        plabels = [l for l in self.protocol_labels if l.refblock > row]
        for pl in plabels:
            pl.refblock += 1

        self.refresh_protolabel_blocks()
        self.qt_signals.line_duplicated.emit()

    def refresh_protolabel_blocks(self):
        self.__group.refresh_labels()

    def fuzz_successive(self):
>>>>>>> b1ae517... Inital Commit
        """
        Führt ein sukzessives Fuzzing über alle aktiven Fuzzing Label durch.
        Sequentiell heißt, ein Label wird durchgefuzzt und alle anderen Labels bleiben auf Standardwert.
        Das entspricht dem Vorgang nacheinander immer nur ein Label aktiv zu setzen.
<<<<<<< HEAD
        """
        self.fuzz(FuzzMode.successive, default_pause=default_pause)

    def fuzz_concurrent(self, default_pause=None):
        """
        Führt ein gleichzeitiges Fuzzing durch, das heißt bei mehreren Labels pro Message werden alle Labels
        gleichzeitig iteriert. Wenn ein Label keine FuzzValues mehr übrig hat,
        wird der erste Fuzzing Value (per Definition der Standardwert) genommen.
        """
        self.fuzz(FuzzMode.concurrent, default_pause=default_pause)

    def fuzz_exhaustive(self, default_pause=None):
        """
        Führt ein vollständiges Fuzzing durch. D.h. wenn es mehrere Label pro Message gibt, werden alle
        möglichen Kombinationen erzeugt (Kreuzprodukt!)
        """
        self.fuzz(FuzzMode.exhaustive, default_pause=default_pause)

    def create_fuzzing_label(self, start, end, msg_index) -> ProtocolLabel:
        fuz_lbl = self.messages[msg_index].message_type.add_protocol_label(start=start, end=end)
        return fuz_lbl

    def set_decoder_for_messages(self, decoder, messages=None):
        raise NotImplementedError("Encoding cant be set in Generator!")

    def to_xml_file(self, filename: str, decoders=None, participants=None, tag_name="fuzz_profile", include_message_types=True, write_bits=True):
        super().to_xml_file(filename=filename, decoders=None, participants=participants, tag_name=tag_name, include_message_types=include_message_types, write_bits=write_bits)

    def from_xml_file(self, filename: str, read_bits=True):
        super().from_xml_file(filename=filename, read_bits=read_bits)

    def clear(self):
        self.messages[:] = []
=======

        :rtype: list of ProtocolBlock
        """
        result = []
        appd_result = result.append
        block_offsets = {}

        for i, block in enumerate(self.blocks):
            labels = [l for l in self.active_fuzzing_labels if l.refblock == i]

            if len(labels) == 0:
                appd_result(block)
                continue

            labels.sort()
            n = sum([len(l.fuzz_values) for l in labels])
            block_offsets[i] = n - 1

            for l in labels:
                l.nfuzzed = n
                for fuzz_val in l.fuzz_values:
                    bool_fuzz_val = [True if bit == "1" else False for bit in fuzz_val]
                    cpy_bits = copy.deepcopy(block.plain_bits)
                    cpy_bits[l.start:l.end] = bool_fuzz_val
                    fuz_block = ProtocolBlock(cpy_bits, block.pause, self.bit_alignment_positions, block.rssi,
                                              block.modulator_indx, block.decoder, [(l.start, l.end)])
                    fuz_block.fuzz_labels = copy.deepcopy(block.fuzz_labels)
                    appd_result(fuz_block)

        # Refblockindizes anpassen
        for l in self.protocol_labels:
            offset = sum(block_offsets[i] for i in block_offsets.keys() if i < l.refblock)
            l.refblock_offset += offset

        self.blocks = result
        """:type: list of ProtocolBlock """
        self.refresh_protolabel_blocks()

    def fuzz_concurrent(self):
        """
        Führt ein gleichzeitiges Fuzzing durch, das heißt bei mehreren Labels pro Block werden alle Labels
        gleichzeitig iteriert. Wenn ein Label keine FuzzValues mehr übrig hat,
        wird der erste Fuzzing Value (per Definition der Standardwert) genommen.

        :rtype: list of ProtocolBlock
        """
        result = []
        appd_result = result.append
        block_offsets = {}

        for i, block in enumerate(self.blocks):
            labels = [l for l in self.active_fuzzing_labels if l.refblock == i]


            if len(labels) == 0:
                appd_result(block)
                continue

            nvalues = numpy.max([len(l.fuzz_values) for l in labels])
            for j in range(nvalues):
                cpy_bits = copy.deepcopy(block.plain_bits)
                fuzz_created = []
                for l in labels:
                    index = j

                    if index >= len(l.fuzz_values):
                        index = 0

                    bool_fuzz_val = [True if bit == "1" else False for bit in l.fuzz_values[index]]
                    cpy_bits[l.start:l.end] = bool_fuzz_val
                    fuzz_created.append((l.start, l.end))

                fuzz_block = ProtocolBlock(cpy_bits, block.pause, self.bit_alignment_positions, block.rssi,
                                           block.modulator_indx, block.decoder, fuzz_created[:])
                fuzz_block.fuzz_labels = copy.deepcopy(block.fuzz_labels)
                appd_result(fuzz_block)

            block_offsets[i] = nvalues - 1
            for l in labels:
                l.nfuzzed = nvalues

        # Refblockindizes anpassen
        for l in self.protocol_labels:
            offset = sum(block_offsets[i] for i in block_offsets.keys() if i < l.refblock)
            l.refblock_offset += offset

        self.blocks = result
        """:type: list of ProtocolBlock """
        self.refresh_protolabel_blocks()

    def fuzz_exhaustive(self):
        """
        Führt ein vollständiges Fuzzing durch. D.h. wenn es mehrere Label pro Block gibt, werden alle
        möglichen Kombinationen erzeugt (Kreuzprodukt!)

        :rtype: list of str
        """
        result = []
        appd_result = result.append
        block_offsets = {}

        for i, block in enumerate(self.blocks):
            labels = [l for l in self.active_fuzzing_labels if l.refblock == i]

            if len(labels) == 0:
                appd_result(block)
                continue

            pool = []
            for l in labels:
                pool.append([(l.start, l.end, fv) for fv in l.fuzz_values])

            n = 0

            for combination in itertools.product(*pool):
                n += 1
                cpy_bits = copy.deepcopy(block.plain_bits)
                fuzz_created = []
                for start, end, fuz_val in combination:
                    bool_fuzz_val = [True if bit == "1" else False for bit in fuz_val]
                    cpy_bits[start:end] = bool_fuzz_val
                    fuzz_created.append((start, end))

                fuz_block = ProtocolBlock(cpy_bits, block.pause, self.bit_alignment_positions, block.rssi,
                                          block.modulator_indx,
                                          block.decoder, fuzz_created)
                fuz_block.fuzz_labels = copy.deepcopy(block.fuzz_labels)
                appd_result(fuz_block)

            block_offsets[i] = n - 1
            for l in labels:
                l.nfuzzed = n

        # Refblockindizes anpassen
        for l in self.protocol_labels:
            offset = sum(block_offsets[i] for i in block_offsets.keys() if i < l.refblock)
            l.refblock_offset += offset

        self.blocks = result
        """:type: list of ProtocolBlock """
        self.refresh_protolabel_blocks()

    def clear(self):
        self.blocks[:] = []
        self.__group.clear_labels()
        self.protocol_labels[:] = []


    def get_label_range(self, lbl: ProtocolLabel, view: int, decode: bool):
        return self.__group.get_label_range(lbl, view, decode)

    def create_fuzzing_label(self, start, end, refblock) -> ProtocolLabel:
        fuz_lbl = self.__group.add_protocol_label(start, end, refblock, 0, False)
        for block in self.blocks:
            block.fuzz_labels.append(fuz_lbl)
        return fuz_lbl

    def remove_label(self, label: ProtocolLabel):
        self.__group.remove_label(label)

    def set_decoder_for_blocks(self, decoder, blocks=None):
        raise NotImplementedError("Encoding cant be set in Generator!")
>>>>>>> b1ae517... Inital Commit
