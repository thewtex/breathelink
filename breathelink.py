import breathe

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import Directive


def breathe_choice(argument):
    """Option defining which breathe directive to use."""
    breathe_directives = [directive for directives in
            breathe.DoxygenDirectiveFactory.directives.iterkeys()]

    return rst.directives.choice(argument, breathe_directives)


class BreathelinkDirective(Directive):

    required_arguments = 1
    option_spec = {
            'breathe': breathe_choice
            }


    def run(self):
        if self.options.has_key('breathe'):
            breathe_directive_name = self.options['breathe']
        else:
            breathe_directive_name = 'doxygenclass'

        arguments = [self.arguments[0]]
        options = {'no-link': ''}
        breathe_directive_class, messages = rst.directives.directive(breathe_directive_name,
                self.state.memo.language, self.state.document)
        self.state.parent += messages
        breathe_directive_instance = breathe_directive_class(breathe_directive_name,
                arguments, options, self.content, self.lineno,
                self.content_offset, self.block_text, self.state, self.state_machine)
        new_content = breathe_directive_instance.run()

        return new_content

def setup(app):

    app.add_directive('breathelink', BreathelinkDirective)
