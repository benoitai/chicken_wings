
import logging

__version__ = '1.0.0'
logger = logging.getLogger()





def launch(run_info, analysis_argv):
    start_time = datetime.datetime.now()
    ret = 0
    
    logger.info(f'PLAYING....')

    curr_time = datetime.datetime.now()
    diff_time = curr_time - start_time
    hours = (diff_time.days * 24) + (diff_time.seconds // 3600)
    minutes = (diff_time.seconds // 60) % 60
    seconds = diff_time.seconds - (60 * minutes)
    logger.info(
        'Run time: {} hours, {} minutes, {} seconds'.format(
            hours, minutes, seconds
        )
    )
    return ret


def process_argv(argv):
    """Parse CLI arguments and return a named tuple object.
    Returns: A SysInfo namedtuple.
    Raises: SystemExit.
    """
    parser = setup_parser()

    args, unknown_argv = parser.parse_known_args(argv)

    if args.data_dir and not args.log_dir:
        # define a default log directory
        args.log_dir = os.path.join(args.data_dir, 'logs')

    args_dict = vars(args)
    attr_list = sorted(args_dict.keys())
    SysInfo = namedtuple('SysInfo', attr_list)
    sys_info = SysInfo(**args_dict)
    return sys_info, unknown_argv



def setup_parser():
    """Define and return argparse ArgumentParser object."""
    parser = argparse.ArgumentParser(description="Welcome to CHICKEN WINGS")
    bili.args.add_log_group(parser)

    in_out_grp = parser.add_argument_group('Output parameters')
    in_out_grp.add_argument(
        '--data-dir',
        default='./data/',
        help='The path to the directory where data should be stored.',
    )

    return parser


def main(argv):
    """Script entrypoint."""
    exit_code = 0

    # generate a namedtuple with all relevant run info
    # -- also starts up logging
    sys_info, analysis_argv = process_argv(argv)
    logger.info('Version {}'.format(__version__))
    logger.info(
        'Called as:\n  {}'.format(
            'main({})'.format(argv) if argv else ' '.join(sys.argv)
        )
    )
    try:
        exit_code = launch(sys_info, analysis_argv)
    except Exception as e:
        logger.exception(str(e))
        exit_code = 1

    return exit_code


if __name__ == '__main__':
    locutus.config()  # setup all loggers

    try:
        retcode = main(sys.argv)
    except SystemExit:
        allowed_exit = ['--version', '-h', '--help']
        if not any(x not in sys.argv for x in allowed_exit):
            logger.error('error parsing arguments')
        raise
    except KeyboardInterrupt:
        logger.critical('early exit--keyboard interrupt')
        sys.exit(1)
    except Exception as e:
        # exit more cleanly
        exc_type, _, _ = sys.exc_info()
        msg = '{}: {}'.format(exc_type.__name__, str(e))
        logger.exception(msg)
        sys.exit(1)
    else:
        sys.exit(retcode)
