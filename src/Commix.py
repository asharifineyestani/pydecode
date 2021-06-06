import os, fnmatch


def reverse_dictionary(dictionary):
    return {v: k for k, v in dictionary.items()}


class Commix:

    def __init__(self, actions):
        self.actions = actions
        self.return_to_original = False

    @staticmethod
    def replace_files(action, find, replace):

        if 'find_pattern' in action:
            find = action['find_pattern'].replace('?', find)
            replace = action['find_pattern'].replace('?', replace)

        if 'file_path' in action:
            if os.path.exists(action['file_path']):
                with open(action['file_path']) as f:
                    s = f.read()
                s = s.replace(find, replace)
                with open(action['file_path'], "w") as f:
                    f.write(s)

        elif 'directory' in action:
            for path, dirs, files in os.walk(os.path.abspath(action['directory'])):
                for filename in fnmatch.filter(files, action['file_pattern']):
                    filepath = os.path.join(path, filename)
                    with open(filepath) as f:
                        s = f.read()
                    s = s.replace(find, replace)
                    with open(filepath, "w") as f:
                        f.write(s)
        return True

    @staticmethod
    def rename_files(action, src, dst):
        for path, dirs, files in os.walk(os.path.abspath(action['directory'])):
            old = os.path.join(path, src + action['file_type'])
            new = os.path.join(path, dst + action['file_type'])
            if os.path.exists(old):
                os.rename(old, new)
        return True


