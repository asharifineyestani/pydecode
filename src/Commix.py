import os, fnmatch


def reverse_dictionary(dictionary):
    return {v: k for k, v in dictionary.items()}


class Commix:

    def __init__(self, actions):
        self.actions = actions
        self.return_to_original = False

    def replace_files(self, action, find, replace):

        if 'find_pattern' in action:
            find = action['find_pattern'].replace('?', find)
            replace = action['find_pattern'].replace('?', replace)

        if 'files' in action:
            if self.return_to_original:
                action['files'].reverse()

            for filepath in action['files']:
                self.replace_in_file(filepath, find, replace)

        elif 'directories' in action:
            if self.return_to_original:
                action['directories'].reverse()

            for directory in action['directories']:
                for path, dirs, files in os.walk(os.path.abspath(directory['path'])):
                    for filename in fnmatch.filter(files, directory['file_pattern']):
                        filepath = os.path.join(path, filename)
                        self.replace_in_file(filepath, find, replace)
        return True

    @staticmethod
    def replace_in_file(filepath, find, replace):
        if os.path.exists(filepath):
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

    @staticmethod
    def rename_files(action, src, dst):
        for path, dirs, files in os.walk(os.path.abspath(action['directory_path'])):
            old = os.path.join(path, src + action['file_type'])
            new = os.path.join(path, dst + action['file_type'])
            if os.path.exists(old):
                os.rename(old, new)
        return True

    def decode(self):
        for action in self.actions:
            if self.return_to_original:
                action['keywords'] = reverse_dictionary(action['keywords'])

            for find, replace in action['keywords'].items():
                if action['type'] == 'replace':
                    self.replace_files(action, find, replace)
                elif action['type'] == 'rename':
                    self.rename_files(action, find, replace)

    def encode(self):
        self.actions.reverse()
        self.return_to_original = True
        return self.decode()
