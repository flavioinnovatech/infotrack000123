from django.forms import Select
from itertools import chain
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import  force_unicode
from itrack.equipments.models import CustomFieldName
from django.conf import settings
from django.utils.datastructures import MultiValueDict, MergeDict

class ColoredSelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        if option_value != '':
            type_to_compare = CustomFieldName.objects.get(pk=int(option_value)).custom_field.type
            color_class = (type_to_compare == 'Output') and u' class="optionred"' or u'class="optiongreen"'
        else:
            color_class = ''
        return u'<option value="%s"%s%s>%s</option>' % (
            escape(option_value), selected_html, color_class,
            conditional_escape(force_unicode(option_label)))


class ColoredSelectMultiple(ColoredSelect):
	    def render(self, name, value, attrs=None, choices=()):
	        if value is None: value = []
	        final_attrs = self.build_attrs(attrs, name=name)
	        output = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
	        options = self.render_options(choices, value)
	        if options:
	            output.append(options)
	        output.append('</select>')
	        return mark_safe(u'\n'.join(output))
	
	    def value_from_datadict(self, data, files, name):
	        print self,data,files,name
	        if isinstance(data, (MultiValueDict, MergeDict)):
	            return data.getlist(name)
	        return data.get(name, None)
	
	    def _has_changed(self, initial, data):
	        if initial is None:
	            initial = []
	        if data is None:
	            data = []
	        if len(initial) != len(data):
	            return True
	        initial_set = set([force_unicode(value) for value in initial])
	        data_set = set([force_unicode(value) for value in data])
	        return data_set != initial_set


class ColoredFilteredSelectMultiple(ColoredSelectMultiple):
	    """
	    A SelectMultiple with a JavaScript filter interface.
	
	    Note that the resulting JavaScript assumes that the jsi18n
        catalog has been loaded in the page
	    """
	    class Media:
	        js = (settings.ADMIN_MEDIA_PREFIX + "js/core.js",
	              settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
	              settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js")
	
	    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
	        self.verbose_name = verbose_name
	        self.is_stacked = is_stacked
	        super(ColoredFilteredSelectMultiple, self).__init__(attrs, choices)
	
	    def render(self, name, value, attrs=None, choices=()):
	        if attrs is None: attrs = {}
	        attrs['class'] = 'selectfilter'
	        if self.is_stacked: attrs['class'] += 'stacked'
	        output = [super(ColoredFilteredSelectMultiple, self).render(name, value, attrs, choices)]
	        output.append(u'<script type="text/javascript">addEvent(window, "load", function(e) {')
	        # TODO: "id_" is hard-coded here. This should instead use the correct
	        # API to determine the ID dynamically.
	        output.append(u'SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n' % \
	            (name, self.verbose_name.replace('"', '\\"'), int(self.is_stacked), settings.ADMIN_MEDIA_PREFIX))
	        return mark_safe(u''.join(output))
