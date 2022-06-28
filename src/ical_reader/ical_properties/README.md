# Property documentation

### DTStamp
    dtstamp    = "DTSTAMP" stmparam ":" date-time CRLF
    stmparam   = *(";" other-param)

### UID
    uid        = "UID" uidparam ":" text CRLF
    uidparam   = *(";" other-param)

### DTStart
    dtstart    = "DTSTART" dtstparam ":" dtstval CRLF
    
    dtstparam  = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" "VALUE" "=" ("DATE-TIME" / "DATE")) /
                   (";" tzidparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

    dtstval    = date-time / date
    ;Value MUST match value type

### Class
    class      = "CLASS" classparam ":" classvalue CRLF

    classparam = *(";" other-param)

    classvalue = "PUBLIC" / "PRIVATE" / "CONFIDENTIAL" / iana-token
                   / x-name
    ;Default is PUBLIC

### Created

    created    = "CREATED" creaparam ":" date-time CRLF

    creaparam  = *(";" other-param)

### Description
    description = "DESCRIPTION" descparam ":" text CRLF

    descparam   = *(
                    ; The following are OPTIONAL, but MUST NOT occur more than once.
                    (";" altrepparam) / (";" languageparam) /
                    ; The following is OPTIONAL, and MAY occur more than once.
                    (";" other-param)
                    )

### Geo
    geo        = "GEO" geoparam ":" geovalue CRLF

    geoparam   = *(";" other-param)

    geovalue   = float ";" float
    ;Latitude and Longitude components

### Last modified
    last-mod   = "LAST-MODIFIED" lstparam ":" date-time CRLF

    lstparam   = *(";" other-param)

### Location
    location   = "LOCATION"  locparam ":" text CRLF

    locparam   = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" altrepparam) / (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )
Example:  The following are some examples of this property:

    LOCATION:Conference Room - F123\, Bldg. 002

    LOCATION;ALTREP="http://xyzcorp.com/conf-rooms/f123.vcf":
     Conference Room - F123\, Bldg. 002

### Organizer

    organizer  = "ORGANIZER" orgparam ":" cal-address CRLF

    orgparam   = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" cnparam) / (";" dirparam) / (";" sentbyparam) /
                   (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )
Example: .... 
     
    ORGANIZER;SENT-BY="mailto:jane_doe@example.com":mailto:jsmith@example.com

### Priority

    priority   = "PRIORITY" prioparam ":" priovalue CRLF
    ;Default is zero (i.e., undefined).

    prioparam  = *(";" other-param)

    priovalue   = integer       ;Must be in the range [0..9]
       ; All other values are reserved for future use.

### Sequence
    seq = "SEQUENCE" seqparam ":" integer CRLF
    ; Default is "0"

    seqparam   = *(";" other-param)

### Status
    status          = "STATUS" statparam ":" statvalue CRLF

    statparam       = *(";" other-param)

    statvalue       = (statvalue-event
                        /  statvalue-todo
                        /  statvalue-jour)

    statvalue-event = "TENTATIVE"    ;Indicates event is tentative.
                        / "CONFIRMED"    ;Indicates event is definite.
                        / "CANCELLED"    ;Indicates event was cancelled.
    ;Status values for a "VEVENT"

    statvalue-todo  = "NEEDS-ACTION" ;Indicates to-do needs action.
                        / "COMPLETED"    ;Indicates to-do completed.
                        / "IN-PROCESS"   ;Indicates to-do in process of.
                        / "CANCELLED"    ;Indicates to-do was cancelled.
    ;Status values for "VTODO".

    statvalue-jour  = "DRAFT"        ;Indicates journal is draft.
                        / "FINAL"        ;Indicates journal is final.
                        / "CANCELLED"    ;Indicates journal is removed.
      ;Status values for "VJOURNAL".

### Summary
    summary    = "SUMMARY" summparam ":" text CRLF

    summparam  = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" altrepparam) / (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Transp
    transp     = "TRANSP" transparam ":" transvalue CRLF

    transparam = *(";" other-param)

    transvalue = "OPAQUE"
                    ;Blocks or opaque on busy time searches.
                    / "TRANSPARENT"
                    ;Transparent on busy time searches.
    ;Default value is OPAQUE

### URL
    url        = "URL" urlparam ":" uri CRLF

    urlparam   = *(";" other-param)

### Recurrence ID
    recurid    = "RECURRENCE-ID" ridparam ":" ridval CRLF

    ridparam   = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" "VALUE" "=" ("DATE-TIME" / "DATE")) /
                   (";" tzidparam) / (";" rangeparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

    ridval     = date-time / date

### RRule
    rrule      = "RRULE" rrulparam ":" recur CRLF

    rrulparam  = *(";" other-param)

### DTEnd
    dtend      = "DTEND" dtendparam ":" dtendval CRLF

    dtendparam = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" "VALUE" "=" ("DATE-TIME" / "DATE")) /
                   (";" tzidparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Duration

    duration   = "DURATION" durparam ":" dur-value CRLF
                     ;consisting of a positive duration of time.

    durparam   = *(";" other-param)

### Attach
    attach     = "ATTACH" attachparam ( ":" uri ) /
                     (
                       ";" "ENCODING" "=" "BASE64"
                       ";" "VALUE" "=" "BINARY"
                       ":" binary
                     )
                     CRLF

    attachparam = *(
                    ;
                    ; The following is OPTIONAL for a URI value,
                    ; RECOMMENDED for a BINARY value,
                    ; and MUST NOT occur more than once.
                    ;
                    (";" fmttypeparam) /
                    ;
                    ; The following is OPTIONAL,
                    ; and MAY occur more than once.
                    ;
                    (";" other-param)
                    ;
                    )

### Attendeee

    attendee   = "ATTENDEE" attparam ":" cal-address CRLF

    attparam   = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" cutypeparam) / (";" memberparam) /
                   (";" roleparam) / (";" partstatparam) /
                   (";" rsvpparam) / (";" deltoparam) /
                   (";" delfromparam) / (";" sentbyparam) /
                   (";" cnparam) / (";" dirparam) /
                   (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Categories

    categories = "CATEGORIES" catparam ":" text *("," text)
                     CRLF

    catparam   = *(
                   ; The following is OPTIONAL,
                   ; but MUST NOT occur more than once.
                   (";" languageparam ) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Comment

    comment    = "COMMENT" commparam ":" text CRLF

    commparam  = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" altrepparam) / (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Contact

    contact    = "CONTACT" contparam ":" text CRLF

    contparam  = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" altrepparam) / (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Exdate

    exdate     = "EXDATE" exdtparam ":" exdtval *("," exdtval) CRLF

    exdtparam  = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" "VALUE" "=" ("DATE-TIME" / "DATE")) /
                   (";" tzidparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

    exdtval    = date-time / date
    ;Value MUST match value type

### Request status

    rstatus    = "REQUEST-STATUS" rstatparam ":"
                     statcode ";" statdesc [";" extdata]

    rstatparam = *(
                   ; The following is OPTIONAL,
                   ; but MUST NOT occur more than once.
                   (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Related to

    related    = "RELATED-TO" relparam ":" text CRLF

    relparam   = *(
                   ; The following is OPTIONAL,
                   ; but MUST NOT occur more than once.
                   (";" reltypeparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Resources
    resources  = "RESOURCES" resrcparam ":" text *("," text) CRLF

    resrcparam = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" altrepparam) / (";" languageparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

### Recurrence date-times
    rdate      = "RDATE" rdtparam ":" rdtval *("," rdtval) CRLF

    rdtparam   = *(
                   ; The following are OPTIONAL, but MUST NOT occur more than once.
                   (";" "VALUE" "=" ("DATE-TIME" / "DATE" / "PERIOD")) /
                   (";" tzidparam) /
                   ; The following is OPTIONAL, and MAY occur more than once.
                   (";" other-param)
                   )

    rdtval     = date-time / date / period
    ;Value MUST match value type

### X-prop
    x-prop = x-name *(";" icalparameter) ":" value CRLF

Example:  The following might be the ABC vendor's extension for an audio-clip form of subject property:

    X-ABC-MMSUBJ;VALUE=URI;FMTTYPE=audio/basic:http://www.example.
     org/mysubj.au


### IANA properties
    iana-prop = iana-token *(";" icalparameter) ":" value CRLF

Example:  The following are examples of properties that might be registered to IANA:

    DRESSCODE:CASUAL

    NON-SMOKING;VALUE=BOOLEAN:TRUE