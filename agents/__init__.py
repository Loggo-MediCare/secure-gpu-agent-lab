"""Safe agent package."""

__all__ = ["run_agent"]


def run_agent(*args, **kwargs):
    from .safe_agent import run_agent as _run_agent

    return _run_agent(*args, **kwargs)
