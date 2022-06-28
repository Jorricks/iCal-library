# Component documentation


## 3.6.1 Event component
       eventc     = "BEGIN" ":" "VEVENT" CRLF
                    eventprop *alarmc
                    "END" ":" "VEVENT" CRLF

       eventprop  = *(
                  ;
                  ; The following are REQUIRED,
                  ; but MUST NOT occur more than once.
                  ;
                  dtstamp / uid /
                  ;
                  ; The following is REQUIRED if the component
                  ; appears in an iCalendar object that doesn't
                  ; specify the "METHOD" property; otherwise, it
                  ; is OPTIONAL; in any case, it MUST NOT occur
                  ; more than once.
                  ;
                  dtstart /
                  ;
                  ; The following are OPTIONAL,
                  ; but MUST NOT occur more than once.
                  ;
                  class / created / description / geo /
                  last-mod / location / organizer / priority /
                  seq / status / summary / transp /
                  url / recurid /
                  ;
                  ; The following is OPTIONAL,
                  ; but SHOULD NOT occur more than once.
                  ;
                  rrule /
                  ;
                  ; Either 'dtend' or 'duration' MAY appear in
                  ; a 'eventprop', but 'dtend' and 'duration'
                  ; MUST NOT occur in the same 'eventprop'.
                  ;
                  dtend / duration /
                  ;
                  ; The following are OPTIONAL, and MAY occur more than once.
                  ;
                  attach / attendee / categories / comment /
                  contact / exdate / rstatus / related /
                  resources / rdate / x-prop / iana-prop
                  ;
                  )
