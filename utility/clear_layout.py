def clear_layout(layout, delete_itself=False):
    if layout is None:
        return

    while layout.count():
        item = layout.takeAt(0)

        if item.widget() is not None:
            item.widget().setParent(None)

        if item.layout() is not None:
            clear_layout(item.layout())

    if delete_itself:
        layout.setParent(None)
