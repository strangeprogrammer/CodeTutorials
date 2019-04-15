from django import forms

from djangocodemirror.fields import CodeMirrorField

class SampleForm(forms.Form):
    foo = CodeMirrorField(label="Foo", required=True,
                          config_name="restructuredtext")
