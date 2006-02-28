from Products.Silva.i18n import translate as _
from Products.Formulator.Errors import FormValidationError

model = context.REQUEST.model
view = context

try:
    result = view.tab_status_form_author.validate_all(context.REQUEST)
except FormValidationError, e:
    return view.tab_status(
        message_type="error", message=view.render_form_errors(e))

# check for status
message=None
if model.get_unapproved_version() is None:
    message=_('There is no unapproved version.')
elif model.is_version_approval_requested():
    message=_('Approval has already been requested.')
# no check for closed ...

editable = model.get_editable()
editable.set_question_start_datetime(result['question_start_datetime'])
editable.set_question_end_datetime(result['question_end_datetime'])
editable.set_result_start_datetime(result['result_start_datetime'])
editable.set_result_end_datetime(result['result_end_datetime'])

if message is not None:
    return view.tab_status(message_type="error", message=message)

import DateTime
context.set_unapproved_version_publication_datetime(DateTime.DateTime())
model.set_unapproved_version_expiration_datetime(None)

model.request_version_approval(result['message'])

if hasattr(model, 'service_messages'):
    model.service_messages.send_pending_messages()
    
return view.tab_status(message_type="feedback", message=_("Approval requested."))