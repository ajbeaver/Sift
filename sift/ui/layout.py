APP_CSS = """
Screen {
    layout: vertical;
}

#chrome {
    height: 1;
}

#browser {
    height: 1fr;
}

#inspect {
    height: 7;
    border-top: solid $primary;
    padding: 0 1;
}

#status {
    height: 1;
    background: $panel;
    color: $text;
    padding: 0 1;
}

#filter {
    display: none;
    height: 3;
}

#filter.visible {
    display: block;
}

#preview-modal {
    width: 90%;
    height: 85%;
    margin: 2 4;
    padding: 1 2;
    background: $surface;
    border: solid $primary;
}

#preview-scroll {
    width: 100%;
    height: 1fr;
    overflow-y: auto;
}

#preview-body {
    width: 100%;
}
"""
