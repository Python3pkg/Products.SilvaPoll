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

viewable = model.get_viewable()
viewable.set_question_start_datetime(result['question_start_datetime'])
viewable.set_question_end_datetime(result['question_end_datetime'])
viewable.set_result_start_datetime(result['result_start_datetime'])
viewable.set_result_end_datetime(result['result_end_datetime'])

return view.tab_status(message_type="feedback", message=_("Dates set."))
