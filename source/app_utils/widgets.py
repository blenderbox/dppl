from django.forms.widgets import CheckboxInput, ClearableFileInput, FileInput
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe


class BetterImageWidget(ClearableFileInput):
    """ This is a better widget for uploading files. """
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': '',
            'input_text': '',
            'clear_template': '',
            'clear_checkbox_label': "Delete",
        }
        template_with_initial = (u'%(initial_text)s %(initial)s '
                                 u'%(clear_template)s<br />%(input_text)s '
                                 u'%(input)s')
        preview_template = ('<a href="%(url)s"><img class="preview" '
                           'src="%(url)s" /></a>')
        template = u'%(input)s'
        substitutions['input'] = super(FileInput, self).render(
                name, value, attrs)

        if value and hasattr(value, "url"):
            template = template_with_initial
            substitutions['initial'] = preview_template % {
                    'url': escape(value.url),
                    }
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                        checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                        checkbox_id)
                substitutions['clear'] = CheckboxInput().render(
                        checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % \
                        substitutions

        return mark_safe(template % substitutions)
