from Products.Silva.i18n import translate as _
from Products.Formulator.Errors import ValidationError, FormValidationError

model = context.REQUEST.model
view = context

if not model.get_unapproved_version():
    # SHORTCUT: To allow approval of closed docs with no new version available,
    # first create a new version. This "shortcuts" the workflow.
    # See also edit/Container/tab_status_approve.py
    if model.is_version_published():
        return view.tab_status(
            message_type="error", 
            message=_("There is no unapproved version to approve."))
    model.create_copy()

try:
    result = view.tab_status_form_editor.validate_all(context.REQUEST)
except FormValidationError, e:
    return view.tab_status(
        message_type="error", message=view.render_form_errors(e))

import DateTime

now = DateTime.DateTime()
model.set_unapproved_version_publication_datetime(now)

editable = model.get_editable()
editable.set_question_start_datetime(result['question_start_datetime'])
editable.set_question_end_datetime(result['question_end_datetime'])
editable.set_result_start_datetime(result['result_start_datetime'])
editable.set_result_end_datetime(result['result_end_datetime'])

model.approve_version()

if hasattr(model, 'service_messages'):
    model.service_messages.send_pending_messages()

return view.tab_status(message_type="feedback", message=_("Version approved."))
