from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from re import compile


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            port = self._locate_SerialNum(match)
            if port:
                for mp in self.mappers:
                    source = self.set_value(mp.source, port, self.used_facts)
                    target = self.set_value(mp.target, port, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
        return relationships

    @staticmethod
    def _locate_SerialNum(line):
        try:
            patern = compile(r'Serial Number: b\'(.+)\'')
            if 'Serial Number:' in line:
                return patern.search(line).group(1)
        except Exception:
            pass
        return None