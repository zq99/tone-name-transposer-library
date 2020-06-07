import unittest
from tonetranspose.transpose import Transpose, NoteNameType, Tone, ToneGroup


def full_range(start, stop): return range(start, stop + 1)


class TestTone(unittest.TestCase):

    def setUp(self):
        pass

    def test_tone_object(self):
        sharp_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        flat_name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        enharmonic_name = ["C", "Db_C#", "D", "Eb_D#", "E", "F", "Gb_F#", "G", "Ab_G#", "A", "Bb_A#", "B"]

        for pitch in full_range(1, 12):
            tone = Tone(pitch)
            self.assertEqual(tone.get_flat_name(), flat_name[pitch - 1])
            self.assertEqual(tone.get_sharp_name(), sharp_name[pitch - 1])
            self.assertEqual(tone.get_enharmonic(), enharmonic_name[pitch - 1])

    def test_tone_instance(self):
        note = "G"
        tone = Tone.get_instance_from_name(note)
        self.assertEqual(tone.get_enharmonic(), "G")


class TestToneGroup(unittest.TestCase):

    def setUp(self):
        pass

    def tone_group_creation(self):
        tone_group = ToneGroup.get_instance_from_input("D", ["D", "F#", "A"])
        self.assertEqual(tone_group.to_string(NoteNameType.Sharp), "D, F#, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Flat), "D, Gb, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Enharmonic), "D, Gb_F#, A")
        self.assertEqual(tone_group.to_string(), "D, Gb_F#, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Sharp), "D, F#, A")


class TestTranspose(unittest.TestCase):

    def setUp(self):
        pass

    def tone_group_summary_intervals(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        intervals = transpose.get_intervals()
        self.assertEquals(intervals, ['R', '3', '5'])

    def tone_group_summary_keys(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        summary_key = transpose.get_tone_groups_by_key_pattern()
        self.assertEqual(len(summary_key), 6)

        keys = ["www", "bwb", "wbw", "bbb", "bww", "wbb"]
        for key in keys:
            if key not in summary_key:
                self.assertRaises(KeyError)

        for key in summary_key:
            if key not in keys:
                self.assertRaises(KeyError)

    def tone_group_summary_data(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        summary_keys = transpose.get_tone_groups_by_key_pattern(NoteNameType.Flat)
        for summary_key in summary_keys:
            if summary_key.key_pattern == "www":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "C,F,G")
            elif summary_key.key_pattern == "bwb":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "Db,Eb,Ab")
            elif summary_key.key_pattern == "wbw":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "D,E,A")
            elif summary_key.key_pattern == "bbb":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "Gb")
            elif summary_key.key_pattern == "bww":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "Bb")
            elif summary_key.key_pattern == "wbb":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "B")

    def test_all_transpositions(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        transpositions = transpose.get_all_positions()
        for t in transpositions:
            pitch = t.root_tone.pitch_number
            if pitch == 1:
                self.assertEqual(t.to_string(), "C, E, G")
            elif pitch == 2:
                self.assertEqual(t.to_string(), "Db_C#, F, Ab_G#")
            elif pitch == 3:
                self.assertEqual(t.to_string(), "D, Gb_F#, A")
            elif pitch == 4:
                self.assertEqual(t.to_string(), "Eb_D#, G, Bb_A#")
            elif pitch == 5:
                self.assertEqual(t.to_string(), "E, Ab_G#, B")
            elif pitch == 6:
                self.assertEqual(t.to_string(), "F, A, C")
            elif pitch == 7:
                self.assertEqual(t.to_string(), "Gb_F#, Bb_A#, Db_C#")
            elif pitch == 8:
                self.assertEqual(t.to_string(), "G, B, D")
            elif pitch == 9:
                self.assertEqual(t.to_string(), "Ab_G#, C, Eb_D#")
            elif pitch == 10:
                self.assertEqual(t.to_string(), "A, Db_C#, E")
            elif pitch == 11:
                self.assertEqual(t.to_string(), "Bb_A#, D, F")
            elif pitch == 12:
                self.assertEqual(t.to_string(), "B, Eb_D#, Gb_F#")


def run_all_tests():
    test_tone = TestTone()
    test_tone.test_tone_instance()
    test_tone_group = TestToneGroup()
    test_tone_group.tone_group_creation()
    test_transpose = TestTranspose()
    test_transpose.tone_group_summary_intervals()
    test_transpose.tone_group_summary_keys()
    test_transpose.tone_group_summary_data()
    test_transpose.test_all_transpositions()
