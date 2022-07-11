# FAQ
???+ "Why did you create this library and not use one of the existing libraries?"

    I first tried several libraries for iCalendar events. However, none of them supported recurring events as well as they should be. For some libraries my calendar loaded but then didn't show my recurring events, while others simply threw stacktraces trying to load it. Furthermore, I noticed that my calendar (with over 2000 events) took ages to load.
    After traversing the code of the other libraries I decided I wanted to build my own. With some key principles that were lacking in most of the libraries:

    - Recurring components should work, always, FOREVER.
    - No strict evaluation that could lead to errors while parsing the file.
    - Lazy evaluation for iCalendar properties to speed up the process.
    - Perfect typing information.
    - Striving for no open issues & especially no open pull requests that are waiting for feedback!

