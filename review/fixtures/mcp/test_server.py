import unittest
from server import call_tool


class NotesTests(unittest.TestCase):
    def test_read_own_workspace(self):
        result = call_tool('list_notes', {'workspace': 'alpha'}, {'subject': 'alice', 'workspace': 'alpha'})
        self.assertEqual(['Alpha roadmap'], result['structuredContent']['notes'])
        self.assertFalse(result['isError'])

    def test_anonymous_denied(self):
        with self.assertRaises(PermissionError):
            call_tool('list_notes', {'workspace': 'alpha'}, None)

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            call_tool('list_notes', {'workspace': 42}, {'subject': 'alice', 'workspace': 'alpha'})


if __name__ == '__main__':
    unittest.main()
