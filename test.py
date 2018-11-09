import git
from git import Repo


repo = Repo(".")

repo.git.checkout("c4023c254b5b4d5b11f0f51ed6f47c54c8673de7")

hc = repo.head.commit

print(hc)
