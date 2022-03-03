import logging

import argparse
from inspect import signature
import asyncio

logger = logging.getLogger(__name__)


def run_command(args: argparse.Namespace):
    """
    Attempts to run a function based on convention.

    Given args contains a `func` attribute pointed to a function,
    attempts to run that function with matching arguments in `args`.
    If `run_async` is specified, will run the function asyncronously
    """
    if not hasattr(args, "func"):
        raise Exception("func was not defined on args")

    func = args.func
    params = signature(func).parameters
    params_input = {
        key: getattr(args, key) for key in params.keys() if hasattr(args, key)
    }

    if hasattr(args, "run_async") and args.run_async:
        logger.debug(
            "run-command-async", extra=dict(command=func.__name__, params=params_input)
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(**params_input))
    else:
        logger.debug(
            "run-command", extra=dict(command=func.__name__, params=params_input)
        )
        func(**params_input)
