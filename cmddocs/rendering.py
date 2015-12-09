""" Class to render ascii from md """
import mistune

class md_to_ascii(mistune.Renderer):
    """ md_to_ascii class """

    def __init__(self, colors):
        mistune.Renderer.__init__(self)
        self.colors = colors

    # Pagelayout
    def block_code(self, code, lang):
        return '\n\033[' + self.colors['code'] + 'm%s\033[0m\n' % code.strip()
    def header(self, text, level, raw=None):
        if level == 2 or level == 1:
            head = '\n\033[4m\033[1m\033[' + self.colors['h1'] + 'm%s\033[0m\n' % text.strip()
        else:
            head = '\n\033[1m\033[' + self.colors['h2'] + 'm%s\033[0m\n' % text.strip()
        return head
    def block_quote(self, text):
        return '\n%s\n' % text.strip()
    def block_html(self, html):
        return '\n%s\n' % html.strip()
    def hrule(self):
        return '---'
    def list(self, body, ordered=True):
        return '\n%s' % body
    def list_item(self, text):
        return '* %s \n'  %  text.strip()
    def paragraph(self, text):
        return '\n%s\n' % text.strip()
    def table(self, header, body):
        return '\n%s\n' % body.strip()
    def table_row(self, content):
        return '\n%s\n' % content.strip()
    def table_cell(self, content, **flags):
        return '\n%s\n' % content.strip()

    # Inline Tags
    def double_emphasis(self, text):
        return '%s' % text.strip()
    def emphasis(self, text):
        return '%s' % text.strip()
    def codespan(self, text):
        return '\n%s\n' % text.strip()
    def linebreak(self):
        return '\n'
    def strikethrough(self, text):
        return '%s' % text.strip()
    def text(self, text):
        return '%s' % text.strip()
    def autolink(self, link, is_email=False):
        return '%s' % link.strip()
    def link(self, link, title, text):
        return '%s (%s)' % (text.strip(), link.strip())
    def image(self, src, title, text):
        return '%s' % src.strip()
    def inline_html(self, html):
        return '%s' % html.strip()
    def newline(self):
        return '\n'
    def footnote_ref(self, key, index):
        return '%s, [%s]' % (key.strip(), index.strip())
    def footnote_item(self, key, text):
        return '%s, [%s]' % (text.strip(), key.strip())
    def footnotes(self, text):
        return '%s' % text.strip()
