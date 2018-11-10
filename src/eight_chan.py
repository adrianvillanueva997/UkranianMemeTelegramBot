from random import randint

import lib.py8chan as py8chan


class EightChanHandler():
    def __init__(self):
        self.chan_8_boards = ['pol', 'v', 'leftypol', 'b', 'tv', 'a', 'christian', 'tech', 'co', 'hgg', 'k', 'newsplus',
                              'r9k',
                              'n',
                              'brit', 'tg', 'monster', 'asmr', 'cuteboys', 'cow', '4chon', 'fur', '4chon', 'sudo',
                              'loli',
                              'aus',
                              'htg', 'animus', 'vore', 'egy', 'erp', 'homosuck', 'shamedsluts', 'abdl', 'abdl', 'pone',
                              'hypno',
                              'strek', 'newbrit', 'test', 'zoo', 'mu', 'fit', 'mexicali', 'waifuist', 'russian',
                              'tijuana',
                              'u', '2hu',
                              'd']

    def random_8_chan_board(self):
        """Returns a random thread given a random board
            Parameters
            ----------
            args : None

            Returns
            -------
            Tuple
                2 Strings with the thread url and caption
            """
        random_board = self.chan_8_boards[randint(0, len(self.chan_8_boards))]
        board = py8chan.board(random_board)
        thread_ids = board.get_all_thread_ids()
        thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
        random_thread = randint(0, (len(thread_ids) - 1))
        thread = board.get_thread(int(thread_ids[random_thread]))
        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        url = 'https://8ch.net/'.__add__(random_board).__add__('/res/').__add__(str(thread_ids[random_thread])).__add__(
            '.html')
        caption = []
        for f in thread.file_objects():
            caption.append(f.file_url)

        print(url, caption[0])
        return url, caption[0]

    def random8_chan_thread(self, args):
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
        board = py8chan.Board(str(query))
        thread_ids = board.get_all_thread_ids()
        thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
        random_thread = randint(0, (len(thread_ids) - 1))
        thread = board.get_thread(int(thread_ids[random_thread]))
        caption = []
        for f in thread.file_objects():
            caption.append(f.file_url)
        url = 'https://8ch.net/'.__add__(str(args)).__add__('/res/').__add__(str(thread_ids[random_thread])).__add__(
            '.html')
        print(url, caption[0])
        return url, caption[0]

    def list_8_chan_boards(self):
        """Returns the list of boards in 8chan
            Parameters
            ----------
            args : None

            Returns
            -------
            List
                All avaliable boards in 8chan
            """
        return self.chan_8_boards
