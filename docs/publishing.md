# Publishing Workflow

This document describes the automated publishing workflow for pydipapi using GitHub Actions.

## Overview

The publishing workflow is designed to automatically build, test, and publish the package to both GitHub Releases and PyPI when version tags are created. The workflow includes several stages for quality assurance and automated deployment.

## Workflow Components

### 1. Continuous Integration (`ci.yml`)

Runs on every push to main branches and pull requests:

- **Linting**: Ruff code formatting and linting checks
- **Security**: Bandit security vulnerability scanning  
- **Type Checking**: MyPy static type checking
- **Testing**: Full test suite across multiple Python versions (3.8-3.12) and operating systems
- **Build Testing**: Validates package can be built and installed
- **Documentation**: Ensures documentation builds successfully

### 2. Release Workflow (`release.yml`)

Triggered when version tags (e.g., `v1.0.0`) are pushed:

- **Testing**: Full test suite validation
- **Building**: Creates wheel and source distributions
- **GitHub Release**: Creates GitHub release with changelog
- **PyPI Publishing**: Publishes to PyPI (production)
- **Test PyPI**: Publishes pre-releases to Test PyPI

### 3. Documentation (`docs.yml`)

Automatically builds and deploys documentation:

- **Building**: Generates documentation with MkDocs
- **Deployment**: Publishes to GitHub Pages
- **Link Checking**: Validates all documentation links

### 4. Dependency Management

- **Dependabot**: Automated dependency updates
- **Auto-merge**: Automatically merges minor/patch updates after CI passes

## Setup Requirements

### 1. GitHub Repository Settings

Enable the following in your GitHub repository settings:

1. **GitHub Pages**: 
   - Go to Settings → Pages
   - Source: GitHub Actions

2. **Environments**:
   - Create a `release` environment
   - Add protection rules (optional: require reviews)

### 2. Secrets Configuration

Add the following secrets in GitHub Settings → Secrets and variables → Actions:

#### Required Secrets

```bash
PYPI_API_TOKEN          # Your PyPI API token
TEST_PYPI_API_TOKEN     # Your Test PyPI API token (optional)
```

#### How to Get PyPI Tokens

1. **PyPI Production Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/token/)
   - Create new API token
   - Scope: Entire account or specific project
   - Copy token and add to GitHub secrets as `PYPI_API_TOKEN`

2. **Test PyPI Token** (optional):
   - Go to [Test PyPI Account Settings](https://test.pypi.org/manage/account/token/)
   - Create new API token
   - Add to GitHub secrets as `TEST_PYPI_API_TOKEN`

### 3. Branch Protection

Set up branch protection rules for `main`:

- Require status checks to pass
- Require pull request reviews
- Restrict pushes to main branch

## Release Process

### Automatic Release (Recommended)

1. **Prepare Release**:
   ```bash
   # Update version in pyproject.toml
   # Update CHANGELOG.md
   git add .
   git commit -m "Prepare release v1.0.0"
   git push origin main
   ```

2. **Create Release Tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Workflow Execution**:
   - CI tests run automatically
   - Package is built and validated
   - GitHub release is created
   - Package is published to PyPI

### Manual Release

Use the workflow dispatch feature:

1. Go to Actions → Release → Run workflow
2. Select branch and trigger manually

## Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)
- `v1.0.0-rc1` - Release candidate
- `v1.0.0-beta1` - Beta release
- `v1.0.0-alpha1` - Alpha release

### Pre-releases

Pre-release versions are automatically published to Test PyPI:

```bash
git tag v1.0.0-rc1
git push origin v1.0.0-rc1
```

## Changelog Management

### Format

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.0.0] - 2025-07-10

### Added
- New feature X
- New feature Y

### Changed
- Modified behavior of Z

### Fixed
- Bug fix for issue #123

### Removed
- Deprecated feature A
```

### Automation

The release workflow automatically:
- Extracts changelog for the current version
- Includes it in GitHub release notes
- Falls back to generic release notes if no changelog entry found

## Quality Gates

### Pre-release Checks

All releases must pass:

- ✅ All tests (multiple Python versions)
- ✅ Code linting (Ruff)
- ✅ Security scanning (Bandit)
- ✅ Type checking (MyPy)
- ✅ Package building validation
- ✅ Documentation building

### Deployment Gates

- **Production PyPI**: Requires `release` environment approval
- **Test PyPI**: Automatic for pre-releases
- **GitHub Releases**: Automatic for all tagged versions

## Monitoring and Troubleshooting

### Workflow Status

Monitor workflow execution:

1. Go to Actions tab in GitHub
2. Check workflow status and logs
3. View detailed step execution

### Common Issues

#### 1. PyPI Upload Fails

**Problem**: `403 Forbidden` or authentication errors

**Solution**:
- Verify `PYPI_API_TOKEN` is correct
- Check token permissions
- Ensure package name is available

#### 2. Test Failures

**Problem**: Tests fail in CI but pass locally

**Solution**:
- Check for environment-specific issues
- Verify all dependencies are specified
- Check Python version compatibility

#### 3. Documentation Build Fails

**Problem**: MkDocs build errors

**Solution**:
- Validate `mkdocs.yml` configuration
- Check for broken internal links
- Verify all documentation dependencies

### Rollback Procedure

If a release needs to be rolled back:

1. **PyPI**: Contact PyPI support (can't delete published versions)
2. **GitHub**: Delete release and tag
3. **Fix**: Create new patch version with fixes

## Best Practices

### 1. Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push and create PR
git push origin feature/new-feature

# 4. Merge after CI passes
# 5. Create release when ready
```

### 2. Release Preparation

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Update documentation if needed
- [ ] Run tests locally
- [ ] Create and push tag

### 3. Security Considerations

- Use scoped PyPI tokens
- Enable 2FA on PyPI account
- Regularly rotate API tokens
- Review dependency updates

## Advanced Configuration

### Custom Deployment Environments

Add additional environments for staging:

```yaml
# .github/workflows/release.yml
environment: staging  # Add staging environment
```

### Matrix Testing

Extend Python version matrix:

```yaml
strategy:
  matrix:
    python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### Custom Build Steps

Add additional build validation:

```yaml
- name: Validate package metadata
  run: |
    python -m twine check dist/*
    python -c "import pydipapi; print(pydipapi.__version__)"
```

## Support

For issues with the publishing workflow:

1. Check [GitHub Actions documentation](https://docs.github.com/en/actions)
2. Review [PyPI publishing guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
3. Open an issue in the repository 