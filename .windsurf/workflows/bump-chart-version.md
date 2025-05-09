---
description: Bump chart version
---

1. If any changes are staged, stash them
2. Bump the patch version in Chart.yaml
3. Create a commit, with the message equaling the version in Chart.yaml (with a v prefix)
4. Tag the commit (with the version from Chart.yaml with a v prefix)
5. Push, with the tags
6. Unstash changes, if any exist