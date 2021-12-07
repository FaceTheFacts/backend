def search_and_locate_element_in_text(text, tag):
    for index in range(len(text)):
        if text[index] == tag[0]:
            if text[index : index + len(tag)] == tag:
                return True, index

    return False, None
