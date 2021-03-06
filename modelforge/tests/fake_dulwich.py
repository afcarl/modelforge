import os
import json
from copy import deepcopy

from dulwich.errors import HangupException, GitProtocolError, NotGitRepository


def clone(remote_url, cached_repo, checkout=True):
    if "not-git-repo" in remote_url:
        raise NotGitRepository
    if "bad-ssh" in remote_url:
        raise HangupException
    if "bad-credentials" in remote_url:
        raise GitProtocolError
    os.makedirs(cached_repo, exist_ok=True)
    with open(os.path.join(cached_repo, "index.json"), "w") as _out:
        json.dump(FakeRepo.index, _out)
    for model in FakeRepo.index["models"]:
        model_dir = os.path.join(cached_repo, model)
        os.makedirs(model_dir, exist_ok=True)
        for uuid in FakeRepo.index["models"][model]:
            with open(os.path.join(model_dir, uuid + ".md"), "w") as _out:
                _out.write("test")
    FakeRepo.remote_url = remote_url
    FakeRepo.checkout = checkout
    FakeRepo.cloned = True


def pull(remote_url, cached_repo):
    FakeRepo.remote_head = "0"
    FakeRepo.pulled = True


def add():
    FakeRepo.added = True


def ls_remote(remote_url):
    return {b"HEAD": "0"}


def commit(message):
    FakeRepo.message = message


def push(cached_repo, remote_url, branch):
    FakeRepo.pushed = True


class FakeRepo:
    _head = "0"
    cloned = False
    checkout = False
    pulled = False
    added = False
    message = None
    pushed = False
    remote_url = None
    index = None

    def __init__(self, cached_repo):
        pass

    @property
    def head(self):
        return self._head

    @classmethod
    def reset(cls, index, head="0"):
        cls.remote_head = "0"
        cls.cloned = False
        cls.checkout = False
        cls.pulled = False
        cls.added = False
        cls.message = None
        cls.pushed = False
        cls.remote_url = None
        cls._head = head
        cls.index = deepcopy(index)
