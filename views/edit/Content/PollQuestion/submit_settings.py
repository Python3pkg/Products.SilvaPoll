from Products.Formulator.Errors import ValidationError, FormValidationError
from Products.Silva.i18n import translate as _

model = context.REQUEST.model
view = context

try:
    result = view.form.validate_all(context.REQUEST)
except FormValidationError, e:
    return view.tab_edit(message_type="error",
                message=context.render_form_errors(e))

try:
    model.save(result['question'], result['answers'])
except:
    return view.tab_edit(message_type='error',
                            message=_(('overwriting values not allowed, '
                                        'either you\'re trying to change the '
                                        'number of answers (not allowed) or '
                                        'you\'re trying to change answers '
                                        'when people have already voted')))

return view.tab_edit(message_type='feedback', message=_('updated'))
