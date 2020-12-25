class movie:

    def __init__(self, title, director, cast, length, rating=None):
        self.title = title
        self.director = director
        self.cast = cast
        self.length = length
        self.rating = rating

    def get_info(self):
        if self.rating is not None:
            return "(Title:%s, Director:%s, Cast:%s, Length:%s, Rating:%s)" % (
            self.title, self.director, self.cast, self.length, self.rating)
        else:
            return "(Title:%s, Director:%s, Cast:%s, Length:%s, Rating:None)" % (
            self.title, self.director, self.cast, self.length)

    def __str__(self):
        return "(%s, %s)" % (self.title, self.director)


class DLLNode:
    def __init__(self, item, prev_node=None, next_node=None):
        self.element = item
        self.next = next_node
        self.prev = prev_node


class PyFlix:
    def __init__(self):
        self.first = DLLNode(None, None, None)
        self.last = DLLNode(None, self.first, None)
        self.first.next = self.last
        self.current = self.first
        self.size = 0

    def __str__(self):
        current_pointer = "-->"
        printer_head = "$$$ PyFlix Library:\n"
        printer_body = ""
        printer_tail = "$$$\n"
        pointer = self.first.next
        while pointer.element is not None:
            if pointer == self.current and self.current is not None:
                printer_body = printer_body + current_pointer + self.current.element.__str__() + "\n"
                pointer = pointer.next
            else:
                printer_body = printer_body + pointer.element.__str__() + "\n"
                pointer = pointer.next
        return printer_head + printer_body + printer_tail

    def add_movie(self, new_movie):
        new_node = DLLNode(new_movie, None, None)
        new_node.next = self.last
        new_node.prev = self.last.prev
        self.last.prev.next = new_node
        self.last.prev = new_node
        self.size = self.size + 1

    def get_current(self):
        return "Current movie:" + self.current.element.__str__()

    def next_movie(self):
        self.current = self.current.next
        if self.current.next is None:
            self.reset()

    def info(self):
        info_head = "Info:"
        info_error = "No current"
        if self.current.element is not None:
            return info_head + self.current.element.get_info() + "\n"
        else:
            return info_error + "\n"

    def prev_movie(self):
        self.current = self.current.prev

    def reset(self):
        self.current = self.first

    def rate(self):
        print(self.get_current())
        input_rate = input("Enter your rating [0 to 4]:")
        self.current.element.rating = input_rate
        print("Your rating was " + input_rate)

    def remove_current(self):
        self.current.next.prev = self.current.prev
        self.current.prev.next = self.current.next
        self.current = self.current.next
        if self.current == self.last:
            self.reset()
        self.size = self.size - 1

    def length(self):
        return self.size

    def search(self, search_word):
        current_node = self.current.element.title
        match_result = 0
        match_error = "No matching movie!"
        while self.current is not None:
            self.next_movie()
            if self.current == self.first:
                self.current = self.first.next
                if search_word in self.current.element.title or \
                        search_word in self.current.element.director or \
                        search_word in self.current.element.cast:
                    match_result += 1
                    return self.current.element
                elif self.current.element.title == current_node:
                    if match_result == 0:
                        return match_error
                    break


#  test
movie1 = movie("El Camino", "Vince Gilligan", "Aaron Paul", 122, None)
movie2 = movie("Joker", "Todd Phillips", "Joaquin Phoenix", 122, None)
movie3 = movie("Midsommar", "An Aster", "Florence Pugh", 138, None)
P = PyFlix()
P.add_movie(movie1)
P.add_movie(movie2)
P.add_movie(movie3)
print(P)
P.next_movie()
print(P.info())
P.next_movie()
print(P.get_current())
P.rate()  # ask the user to rate the current movie
print(P)
P.prev_movie()  # move the current pointer to the previous movie
P.remove_current()  # delete the current movie
print(P)  # display the full list to the screen
print(P.info())  # display the info for the current movie
movie4 = movie("Hustlers", "Lorene Scafaria", "Constance Wu, Jennifer Lopez", 110, None)
P.add_movie(movie4)  # create the movie4 and add it
P.next_movie()  # move current pointer to the next movie
P.next_movie()  # move current pointer to the next movie
print(P.info())
print(P)
print(P.search("Joker"))
