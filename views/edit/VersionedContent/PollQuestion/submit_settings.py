from Products.Formulator.Errors import ValidationError, FormValidationError
from Products.Silva.i18n import translate as _

model = context.REQUEST.model
version = model.get_editable()
view = context

try:
    result = view.form.validate_all(context.REQUEST)
except FormValidationError, e:
    return view.tab_edit(message_type="error",
                message=context.render_form_errors(e))

version.set_title(result['object_title'])

try:
    version.save(result['question'], result['answers'], True)
except model.get_OverwriteNotAllowed():
    # note that we don't add an i18n domain since the message is exactly the
    # same as in the core (this does mean it needs to be kept in sync, though!)
    return view.tab_edit(message_type='error',
                            message=_(('overwriting values not allowed, '
                                        'either you\'re trying to change the '
                                        'number of answers (not allowed) or '
                                        'you\'re trying to change answers '
                                        'when people have already voted')))
except model.get_TooManyAnswers():
    return view.tab_edit(message_type='error',
                            message=_(('you have exceeded the maximum of 20 '
                                        'allowed answers')))

return view.tab_edit(message_type='feedback', message=_('updated'))
