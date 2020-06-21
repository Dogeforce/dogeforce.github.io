from io import TextIOWrapper
from datetime import datetime, date


class MarkdownWithMetadata:
    metadata: dict
    content: str

    def __init__(self, md, c):
        self.metadata = md
        self.content = c

    def __str__(self):
        return '{} attributes: {}'.format(len(list(self.metadata)), ', '.join(list(self.metadata)))

    def __getattr__(self, attrname):
        if attrname in self.metadata:
            if 'date' in attrname and type(self.metadata[attrname]) != date:
                datestrs = self.metadata[attrname].split('-')[-3:]
                self.metadata[attrname] = datetime(
                    int(datestrs[0]),
                    int(datestrs[1]),
                    int(datestrs[2])
                ).date()
            return self.metadata[attrname]
        return ''


def parse_markdown(md: TextIOWrapper):
    parsing = False
    metadata = {}
    lines = []
    for line in md.readlines():
        if line == '---\n' and not parsing and len(lines) == 0:
            parsing = not parsing
            continue
        elif line == '---\n' and parsing:
            parsing = not parsing
            continue

        if parsing:
            line_data = line.split(': ')
            attr = line_data[0]
            attr_data = ''.join(line_data[1:])
            metadata[attr] = attr_data.replace('\n', '')

        else:
            lines.append(line)

    return MarkdownWithMetadata(metadata, ''.join(lines))
