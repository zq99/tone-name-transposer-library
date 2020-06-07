import enum


def full_range(start, stop): return range(start, stop + 1)


class NoteNameType(enum.Enum):
    Flat = 1
    Sharp = 2
    Enharmonic = 3


class SortKeys(enum.Enum):
    KeyPattern = 1
    Count = 2
    WhiteCount = 3
    BlackCount = 4


class Direction(enum.Enum):
    Ascending = 1
    Descending = 2


class PianoKeys:
    def __init__(self, key_pattern, count, root_notes, notes_list):
        self.key_pattern = key_pattern
        self.count = count
        self.root_notes = root_notes
        self.notes_list = notes_list
        self.white_count = key_pattern.count('w')
        self.black_count = key_pattern.count('b')


class Tone:
    min_pitch = 1
    max_pitch = 12
    location = ["w", "b", "w", "b", "w", "w", "b", "w", "b", "w", "b", "w"]
    sharp_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    flat_name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    def __init__(self, pitch_number):
        if Tone.is_valid_pitch(pitch_number):
            self.pitch_number = pitch_number
        else:
            print("value for pitch number not valid: ", pitch_number)
            raise ValueError

    @staticmethod
    def is_valid_pitch(pitch_number):
        return Tone.min_pitch <= pitch_number <= Tone.max_pitch

    @staticmethod
    def get_instance_from_name(note_name):
        if note_name in Tone.sharp_name:
            return Tone(Tone.sharp_name.index(note_name) + 1)
        elif note_name in Tone.flat_name:
            return Tone(Tone.flat_name.index(note_name) + 1)
        else:
            print("note name does not exist: ", note_name)
            raise ValueError

    def get_location_on_keyboard(self):
        return self.location[self.pitch_number - 1]

    def get_sharp_name(self):
        return self.sharp_name[self.pitch_number - 1]

    def get_flat_name(self):
        return self.flat_name[self.pitch_number - 1]

    def get_enharmonic(self):
        if self.get_flat_name() == self.get_sharp_name():
            return self.get_flat_name()
        else:
            return self.get_flat_name() + "_" + self.get_sharp_name()

    def get_note_name(self, note_name_type):
        if note_name_type == NoteNameType.Flat:
            return self.get_flat_name()
        elif note_name_type == NoteNameType.Sharp:
            return self.get_sharp_name()
        else:
            return self.get_enharmonic()


class ToneGroup:
    __to_string = ""

    def __init__(self, root_tone, tone_list, tone_pattern, key_pattern):
        self.root_tone = root_tone
        self.tone_list = tone_list
        self.tone_pattern = tone_pattern
        self.key_pattern = key_pattern
        self.note_name_type = NoteNameType.Enharmonic

    @staticmethod
    def get_instance_from_input(root_note, note_name_list):
        root_tone = Tone.get_instance_from_name(root_note)
        tone_list = []
        tone_pattern = []
        key_pattern = ""
        for name in note_name_list:
            note_tone = Tone.get_instance_from_name(name)
            tone_list.append(note_tone)
            key_pattern += note_tone.get_location_on_keyboard()
            interval = note_tone.pitch_number - root_tone.pitch_number
            tone_pattern.append(interval)
        return ToneGroup(root_tone, tone_list, tone_pattern, key_pattern)

    def to_string(self, note_name_type=None):
        if self.tone_list:
            note_type = note_name_type if note_name_type is not None else self.note_name_type
            if self.__to_string == "" or note_type != self.note_name_type:
                self.__to_string = ', '.join((tone.get_note_name(note_type) for tone in self.tone_list))
                self.note_name_type = note_type
        return self.__to_string


class Transpose:

    def __init__(self, root, notes_list):
        self.root = root
        self.notes_list = notes_list
        self.transposed_list = []
        self.piano_key_list = []
        self.intervals_list = []
        self.note_name_type = NoteNameType.Enharmonic

    @staticmethod
    def __get_interval(root_pitch, steps):
        if Tone.is_valid_pitch(root_pitch):
            transposed_pitch = (Tone.max_pitch + steps) + root_pitch if steps < 0 else root_pitch + steps
            return transposed_pitch if transposed_pitch <= Tone.max_pitch else transposed_pitch - Tone.max_pitch
        else:
            raise ValueError

    def get_all_positions(self):
        if not self.transposed_list:
            tone_group = ToneGroup.get_instance_from_input(self.root, self.notes_list)
            for pitch_number in full_range(Tone.min_pitch, Tone.max_pitch):
                if pitch_number == tone_group.root_tone.pitch_number:
                    self.transposed_list.append(tone_group)
                else:
                    root_tone = Tone(pitch_number)
                    transposed = []
                    key_pattern = ""
                    for part in tone_group.tone_pattern:
                        transposed_pitch_number = self.__get_interval(pitch_number, part)
                        transposed_tone = Tone(transposed_pitch_number)
                        transposed.append(transposed_tone)
                        key_pattern += transposed_tone.get_location_on_keyboard()
                    self.transposed_list.append(ToneGroup(root_tone, transposed, tone_group.tone_pattern, key_pattern))
        return self.transposed_list

    def get_tone_groups_by_key_pattern(self, note_name_type=None, sort_keys=SortKeys.Count,
                                       direction=Direction.Descending):
        if not self.transposed_list:
            self.get_all_positions()

        note_type = self.__get_valid_note_name_type(note_name_type)

        piano_key_dict = {}
        tone_positions = self.get_all_positions()
        for position in tone_positions:
            if position.key_pattern not in piano_key_dict:
                tone_list = [position]
                piano_key_dict[position.key_pattern] = tone_list
            else:
                piano_key_dict[position.key_pattern].append(position)

        for key in piano_key_dict:
            root_names = ",".join([x.root_tone.get_note_name(note_type) for x in piano_key_dict[key]])
            piano_keys = PianoKeys(key, len(piano_key_dict[key]), root_names, piano_key_dict[key])
            self.piano_key_list.append(piano_keys)
        self.__sort_piano_key_list(sort_keys, direction)

        return self.piano_key_list

    def __sort_piano_key_list(self, sort_keys, direction):
        if self.piano_key_list:
            direction = True if direction == Direction.Descending else False
            if sort_keys == SortKeys.KeyPattern:
                self.piano_key_list.sort(key=lambda piano_key: piano_key.key_pattern, reverse=direction)
            elif sort_keys == SortKeys.WhiteCount:
                self.piano_key_list.sort(key=lambda piano_key: piano_key.white_count, reverse=direction)
            elif sort_keys == SortKeys.BlackCount:
                self.piano_key_list.sort(key=lambda piano_key: piano_key.black_count, reverse=direction)
            else:
                self.piano_key_list.sort(key=lambda piano_key: piano_key.count, reverse=direction)

    def print_key_pattern(self, note_name_type=None, sort_keys=SortKeys.Count,
                          direction=Direction.Descending):
        note_type = self.__get_valid_note_name_type(note_name_type)
        key_patterns = self.get_tone_groups_by_key_pattern(note_type, sort_keys, direction)
        if key_patterns:
            for keys in key_patterns:
                print(keys.key_pattern, "|", keys.count, "|", keys.root_notes)

    def print_positions(self, note_name_type=None):
        positions = self.get_all_positions()
        note_type = self.__get_valid_note_name_type(note_name_type)
        if positions:
            for position in positions:
                print(position.root_tone.get_note_name(note_type), "|", position.to_string(note_type))

    @staticmethod
    def get_interval_label(distance_root_to_note, note_name_type=None):
        labels_flat = {0: "R", 1: "b2", 2: "2", 3: "b3", 4: "3", 5: "4", 6: "b5", 7: "5", 8: "b6", 9: "6", 10: "b7",
                       11: "7", 12: "R"}
        labels_sharp = {0: "R", 1: "#R", 2: "2", 3: "#2", 4: "3", 5: "4", 6: "#4", 7: "5", 8: "#5", 9: "6", 10: "#6",
                        11: "7", 12: "R"}

        if note_name_type is None:
            note_name_type = NoteNameType.Enharmonic

        distance = distance_root_to_note if distance_root_to_note >= 0 else (
                Tone.max_pitch + distance_root_to_note)
        if (Tone.min_pitch - 1) <= distance <= Tone.max_pitch:

            if note_name_type == NoteNameType.Sharp:
                return labels_sharp[distance]
            elif note_name_type == NoteNameType.Flat:
                return labels_flat[distance]
            else:
                if labels_flat[distance] == labels_sharp[distance]:
                    return labels_flat[distance]
                else:
                    return labels_sharp[distance] + "_" + labels_flat[distance]
        else:
            return distance_root_to_note

    def get_intervals(self, note_name_type=None):
        note_type = self.__get_valid_note_name_type(note_name_type)
        if not self.intervals_list or self.note_name_type is not note_type:
            self.note_name_type = note_type
            root_tone = Tone.get_instance_from_name(self.root)
            for note in self.notes_list:
                tone = Tone.get_instance_from_name(note)
                self.intervals_list.append(
                    self.get_interval_label(tone.pitch_number - root_tone.pitch_number, note_type))
        return self.intervals_list

    def print_intervals(self, note_name_type=None):
        print(self.get_intervals(self.__get_valid_note_name_type(note_name_type)))

    def __get_valid_note_name_type(self, note_name_type):
        return note_name_type if note_name_type is not None else self.note_name_type
