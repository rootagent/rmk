# The CLI entrypoint to root monkey (rmk).

import argparse
import logging
import os
import signal
import sys
from pathlib import Path

from rmonkey import AskAgent, RootMonkey, SWEAgent, __version__
from rmonkey.utils import os_info, user_rules
from rmonkey.utils.pretty_console import PrettyConsole
from rmonkey.utils.util import generate_session_id

logger = logging.getLogger(__name__)

agent: AskAgent | SWEAgent | RootMonkey = None
agent_log_dir = Path.cwd() / ".rmk" / "traj"


def _register_signal_handlers():
    def signal_handler(signum, frame):
        logger.debug(f"Received {signum} signal.")
        logger.info(f"Saved trajectory to {agent_log_dir} and exiting...")
        global agent
        traj_file = agent.save(agent_log_dir)
        print(f"Saved agent trajectory to {traj_file} and exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTSTP, signal_handler)  # Handle Ctrl+Z


def main():
    _register_signal_handlers()
    parser = argparse.ArgumentParser(description="RootMonkey CLI.")

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit",
    )
    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        default="dev",
        choices=["ask", "agent", "dev"],
        required=False,
        help="RMK mode: ask, agent, or dev. default is 'dev'.",
    )
    parser.add_argument(
        "--task",
        "-t",
        type=str,
        help="user's input task.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output to observe LLM behavior.",
    )
    args = parser.parse_args()

    global agent
    console = PrettyConsole()
    session_id = generate_session_id()
    verbose = args.verbose

    def get_task_from_arg(task_arg):
        if task_arg and os.path.isfile(task_arg):
            with open(task_arg, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return task_arg

    if args.mode == "ask":
        agent = AskAgent()
        while True:
            try:
                input_message = input("RMK[ask] > ")
                if not input_message.strip():
                    console.print("Input cannot be empty. Please try again.")
                    continue
                if input_message.strip().lower() in ["/exit", "/quit"]:
                    traj_file = agent.save(agent_log_dir)
                    print(f"Saved ask history to {traj_file} and exiting...")
                    return
                result = agent.run(input_message)
                console.print(f"Agent Result:\n{result}", "assistant")
            except Exception as e:
                print(str(e))
                return
    elif args.mode == "agent":
        agent = SWEAgent()
        input_task = get_task_from_arg(args.task)
        while True:
            try:
                if not input_task:
                    input_task = input("RMK[agent] > ")
                    if not input_task.strip():
                        console.print("Input task cannot be empty. Please try again.")
                        continue
                result = agent.run(input_task)
                console.print(f"RMK[agent] > \n{result}")
                input_message = input("RMK[agent] > ")
                if input_message.strip().lower() in ["/exit", "/quit"]:
                    traj_file = agent.save(agent_log_dir)
                    print(f"Saved agent trajectory to {traj_file} and exiting...")
                    return
            except Exception as e:
                print(str(e))
                return
    elif args.mode == "dev":
        system_ctx = os_info.system()
        user_rules_ctx = user_rules.load_rmk_rules(os.getcwd())
        if user_rules_ctx:
            system_ctx = f"{system_ctx}\n{user_rules_ctx}"
        agent = RootMonkey(system_rules=system_ctx, session_id=session_id, verbose=verbose, console=console)
        input_task = get_task_from_arg(args.task)
        try:
            if not input_task:
                while True:
                    input_task = input("RMK[dev] > ")
                    if not input_task.strip():
                        console.print("Input task cannot be empty. Please try again.")
                    else:
                        break
            result = agent.run(input_task)
            console.print(f"RMK[dev] > {result}", "assistant")
            traj_file = agent.save(agent_log_dir)
            print(f"Saved dev trajectory to {traj_file} and exiting...")
        except Exception as e:
            print(str(e))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
