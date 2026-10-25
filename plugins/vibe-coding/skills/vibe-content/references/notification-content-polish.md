# Improve Notification Content

## Scope

Correct the selected template, language, interpolation or destination at its maintained source. Preserve eligibility, consent, channel and delivery semantics unless changing them is part of the request.

## Procedure

1. Establish the state/audience the message represents and the supported action. Fix false or stale claims against the actual producer.
2. Update directly affected templates/locales with safe variable handling, escaping, plural rules and channel constraints.
3. Keep sensitive payloads and internal diagnostics out of visible text and links. Ensure the destination remains authorized for the intended recipient.

## Verification

Render representative synthetic inputs, missing/invalid values and selected success/failure/expired states in the affected channel/locales. Check links and accessibility where relevant. Report preview evidence and provider/channel rendering not exercised; do not send a live message to validate wording.

Use the same event/recipient fixture before and after the correction, including the supported destination/expiry condition. Verify the rendered body and actual link target, not only the translation key. A failed preview returns to the template/data mapping owner; accepted wording proceeds to Patch Checking. Consent or delivery changes remain with their own authorized workflow.
