

class Utils:

    @staticmethod
    def get_input_file(fname):
        with open(fname) as f:
            content = f.readlines()
        # remove whitespace characters and `\n` at the end of each line
        content = [x.strip() for x in content]
        return content
