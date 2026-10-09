# User interaction states

Choose states by the product contract first; do not mechanically fit every component with a full state machine. A saveable list usually needs the following observable boundaries:

| State/event | Page and action | Result to prove |
| --- | --- | --- |
| Initial read/refresh | loading or an explicit refresh marker; forbid operations that act on an unknown object | Content of the old filter does not pass as the current result |
| Successful empty list | Show no results and a legitimate next step | An empty array is not treated as an error; the page number stays valid |
| Editable/read-only | Hide or disable per product requirements; the explanation for disabling is accessible | Keyboard/shortcut actions cannot accidentally send write requests either |
| Saving | Set pending as soon as click handling starts | Consecutive clicks produce only the expected number of submits |
| Save failure/conflict | Keep the draft; safe error and a recoverable action | A business rejection is not disguised as success; a conflict is not silently overwritten |
| Auth expired | Clear data that may no longer be shown; prompt per the login/authorisation contract | The server still owns authorisation; the client does not cache and leak old-permission data |
| Leave/unmount | Handle per the unsaved-changes contract; release this component's resources | A late response does not change the new page; cancel does not claim to undo a submitted write |

For saving, use explicit state instead of relying on button disabled alone: the event handler itself checks pending synchronously; multiple entry points share the same pending or operation identity;
disabling is only UI feedback. If parallel saves of different objects are really allowed, isolate state by object identity; one global boolean must not wrongly block unrelated operations.

Sensitive values use an explicit "keep/replace/clear" contract; a placeholder is not the original value, and a blank default must not be inferred as clear.
Send only the fields authorisation allows changing; hiding a button is user experience, while rejection of direct requests and field trimming must be proven by the server.

Before retrying, distinguish: reads can be retried; an explicit rejection can be retried after correction; an unknown write result needs a query/idempotency contract.
Do not clear the draft on network failure, and do not generate a new operation identity on every user retry, which causes duplicate creation.

For dialogs, verify focus entry, keyboard close and return to the trigger;
DOM unit tests can verify attributes and events, but occlusion, real focus traversal, layout and native browser constraints need the browser layer.
A small copy change verifies only the related copy and accessible name; do not take the opportunity to refactor the dialog.

Normal example: a failed save keeps the input; the user corrects the field and submits a second time; success triggers exactly one reload.
Counterexample: the button only pops "success" with no service call; the form still closes on a backend rejection; the page is readonly but the shortcut keeps saving.
