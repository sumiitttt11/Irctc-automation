# ─────────────────────────────────────────────
#  SELECTOR REGISTRY
#  Update this file when IRCTC changes its DOM.
#  All modules import from here — never hardcode.
# ─────────────────────────────────────────────

# ── Login ──────────────────────────────────────
LOGIN_LINK         = "a[aria-label='Click here to Login in application']"
LOGIN_MODAL        = ".irmodal"
LOGIN_FORM         = ".irmodal form"
INPUT_USERNAME     = "input[formcontrolname='userid']"
INPUT_PASSWORD     = "input[formcontrolname='password']"
SUBMIT_BTN         = "button[type='submit']"
CAPTCHA_IMG        = "app-captcha img, img[src*='captcha'], .captchaContainer img"
CAPTCHA_INPUT      = "input[formcontrolname='captcha'], input[placeholder*='aptcha']"

# ── Train search ───────────────────────────────
FROM_STATION_INPUT = "input[aria-label='Enter From station. Input is Mandatory.']"
TO_STATION_INPUT   = "input[aria-label='Enter To station. Input is Mandatory.']"
AUTOCOMPLETE_ITEMS = 'ul[role="listbox"] li'
DATE_INPUT         = '[formcontrolname="journeyDate"] input'
CALENDAR_MONTH     = '.ui-datepicker-month'
CALENDAR_YEAR      = '.ui-datepicker-year'
CALENDAR_NEXT      = '.ui-datepicker-next'
CALENDAR_DAYS      = '.ui-datepicker-calendar a'
QUOTA_DROPDOWN     = '[formcontrolname="journeyQuota"] .ui-dropdown'
DROPDOWN_ITEMS     = '.ui-dropdown-item'
SEARCH_BTN         = 'button[type="submit"].search_btn.train_Search'

# ── Train selector ─────────────────────────────
TRAIN_CARDS        = "app-train-avl-enq"
CLASS_BOX          = "div.pre-avl"
BOOK_NOW_BTN       = "button"           # scoped to train card

# ── Passenger filler ──────────────────────────
PASSENGER_ROW      = "app-passenger"
NAME_INPUT         = "input[placeholder='Name']"
AGE_INPUT          = "input[placeholder='Age']"
GENDER_SELECT      = "select[formcontrolname='passengerGender']"
MASTER_LIST_ITEM   = "li[role='option']"
AUTO_UPGRADE_CB    = "input#autoUpgradation"
CONTINUE_BTN       = "button.train_Search.btnDefault"
ADD_PASSENGER_TEXT = "Add Passenger"

# ── Payment page ──────────────────────────────
PAYMENT_UPI_OPTION = "label[for*='upi'], .upiRadio, input[value='UPI']"
SAVED_UPI_DROPDOWN = "select[formcontrolname='savedVpa'], .upi-select"
PAY_NOW_BTN        = "button.btnDefault, button[class*='pay']"
PNR_CONFIRM_TEXT   = ".pnrNo, .booking-done, span[class*='pnr']"
IRCTC_TIMEOUT_MODAL = ".errorMessage, .timeout-modal"
