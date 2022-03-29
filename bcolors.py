class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#   
def printColor(color:bcolors,msg):
    """
    Sum up two integers
    Arguments:
        a: an integer
        b: an integer
    Returns:
        The sum of the two integer arguments
    """
    print(f"{color}{msg}{bcolors.ENDC}")