# Release Process

## Version Management

This project uses `hatch-vcs` — the git tag is the single source of truth for
the version. There is no version string in any file to maintain manually.

## Prerequisites

### PyPI Trusted Publishing (one-time setup)

Both Test PyPI and PyPI use OIDC trusted publishing (no API tokens needed).

> **Requires the *Owner* role on the project.** The publishing settings are not
> available to Maintainers — if you only have the Maintainer role, ask an owner
> to add the publisher (or to promote you). On a project that does not exist
> yet, an owner can instead create a *pending publisher*, which is converted
> into a regular one by the first successful upload.

1. **Test PyPI**: https://test.pypi.org/manage/project/collective.easyformplugin.registration/settings/publishing/
   - Add a GitHub publisher: owner=`collective`,
     repo=`collective.easyformplugin.registration`,
     workflow=`release.yaml`, environment=`release-test-pypi`

2. **PyPI**: https://pypi.org/manage/project/collective.easyformplugin.registration/settings/publishing/
   - Add a GitHub publisher: owner=`collective`,
     repo=`collective.easyformplugin.registration`,
     workflow=`release.yaml`, environment=`release-pypi`

3. **GitHub Environments**: In the repo settings, create two environments:
   - `release-test-pypi`
   - `release-pypi` (optionally add required reviewers for extra safety)

## Making a Release

Do not finalize the changelog heading before the PyPI publisher is in place —
otherwise the repository claims a released version that cannot be uploaded.
Until then, `master` keeps publishing dev builds to Test PyPI on every green
CI run, which is a fine preview.

### 1. Finalize the changelog

Every change lands in `CHANGES.md` under the open `## x.y.z (unreleased)`
section. To release, promote that heading to the plain version:

```markdown
## 3.0.0
```

Commit that to `master` (via a short PR if direct pushes are blocked):

```bash
git checkout -b release/3.0.0
git commit -am "Finalize CHANGES for 3.0.0 release"
git push -u origin release/3.0.0
```

### 2. Wait for CI

CI must be green on `master`. A green `master` run also uploads a dev build to
Test PyPI, so you can check the artifact there before releasing.

### 3. Tag and publish

```bash
git checkout master && git pull
git tag -a 3.0.0 -m "Release 3.0.0"
git push origin 3.0.0
```

Then create a GitHub Release from that tag (release notes = the changelog
section). Publishing the release triggers `release.yaml`, which uploads the
package to PyPI.

### 4. Verify and reopen the changelog

- Check https://pypi.org/project/collective.easyformplugin.registration/
- Add a new `## x.y.z (unreleased)` section at the top of `CHANGES.md`.

## Troubleshooting

- **Version is wrong / says `0.1.dev…`**: the checkout has no tags. All
  workflows use `fetch-depth: 0`; keep it that way — `hatch-vcs` derives the
  version from the git history.
- **Test PyPI upload did not run**: it is triggered by `workflow_run` on the
  workflow named exactly **CI**. Renaming that workflow breaks the trigger.
- **PyPI rejects the upload**: trusted publishing must match repo, workflow
  filename and environment name exactly (see above).
