from random import randint

import basc_py4chan


class FourChanHandler():
    def __init__(self):
        self.boards = ['3', 'a', 'aco', 'adv', 'an', 'asp', 'b', 'bant', 'biz', 'c', 'cgl', 'ck', 'cm', 'd', 'diy', 'e',
                       'f',
                       'fa',
                       'fit', 'g', 'gd', 'gif', 'h', 'hc', 'his', 'hm', 'hr', 'i', 'ic', 'int', 'jp', 'k', 'lgbt',
                       'lit',
                       'm', 'mlp',
                       'mu', 'n', 'news', 'o', 'out', 'p', 'po', 'pol',
                       'qa', 'gat', 'r', 'r9k', 's', 's4s', 'sci', 'soc', 'sp', 't', 'tg', 'toy', 'trash', 'trv', 'tv',
                       'u',
                       'v',
                       'vg', 'vp', 'vr', 'w', 'wsg', 'wsr', 'x', 'y']

    def check4_chan_board(self, args):
        """Returns the active threads in a certain board
            Parameters
            ----------
            args : string
                Board to check

            Returns
            -------
            tuple
                Active threads in a certain board
            """
        query = ' '.join(args)
        board = basc_py4chan.Board(query)
        thread_ids = board.get_all_thread_ids()
        message = 'There are: ' + str(len(thread_ids)) + ' active threads on: ' + str(query)
        return message

    def random_thread(self, args):
        """Returns a random thread given a board
            Parameters
            ----------
            args : String
                Board

            Returns
            -------
            Tuple
                2 Strings with the thread url and caption
            """
        query = ' '.join(args)
        board = basc_py4chan.Board(str(query))
        thread_ids = board.get_all_thread_ids()
        thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
        random_thread = randint(0, (len(thread_ids) - 1))
        thread = board.get_thread(int(thread_ids[random_thread]))
        pictures = []
        url = r'http://boards.4chan.org/'.__add__(str(query)).__add__('/thread/').__add__(str(thread_ids[random_thread]))
        for f in thread.file_objects():
            pictures.append(f.file_url)

        return url, pictures[0]

    def random_board(self):
        """Returns a random thread given a random board
            Parameters
            ----------
            args : None


            Returns
            -------
            Tuple
                2 Strings with the thread url and caption
            """
        random_board = self.boards[randint(0, 68)]
        board = basc_py4chan.board(random_board)
        thread_ids = board.get_all_thread_ids()
        thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
        random_thread = randint(0, (len(thread_ids) - 1))
        thread = board.get_thread(int(thread_ids[random_thread]))
        pictures = []
        for f in thread.file_objects():
            pictures.append(f.file_url)
        url = r'http://boards.4chan.org/'.__add__(str(random_board)).__add__('/thread/').__add__(
            str(thread_ids[random_thread]))
        return url, pictures[0]

    def list_4_chan_boards(self):
        """Returns the list of boards in 8chan
            Parameters
            ----------
            args : None

            Returns
            -------
            List
                All avaliable boards in 8chan
            """
        return self.boards
