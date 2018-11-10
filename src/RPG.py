import random


def roll_the_dice(args):
    """Rolls the dice!
        Parameters
        ----------
        args : Integer
            Higher value of the dice that we want to roll

        Returns
        -------
        Integer
            Random number
        """
    number = ' '.join(args)
    if float(number) == 0:
        return 0
    else:
        number = random.randint(1,float(number))
        return number