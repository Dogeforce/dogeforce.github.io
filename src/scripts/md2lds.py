from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class LDSProcessor(Treeprocessor):

    def run(self, root):
        for child in root:
            self._apply(child)

    def _apply(self, el):
        if el.tag == 'h1':
            el.set('class', 'slds-text-heading_large slds-m-bottom_medium slds-m-top_medium')
        elif el.tag == 'h2':
            el.set('class', 'slds-text-heading_medium slds-m-bottom_medium slds-m-top_medium')
        elif el.tag == 'h3':
            el.set('class', 'slds-text-heading_small slds-m-bottom_medium slds-m-top_medium')
        elif el.tag == 'p':
            el.set('class', 'slds-m-bottom_medium')
        elif el.tag == 'blockquote':
            el.set('class', 'slds-border_left slds-p-left_small')



class Md2Lds(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(LDSProcessor(), 'LDSProcessor', 100)
