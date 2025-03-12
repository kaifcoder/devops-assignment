
## Latest Changes
**Changelog for Release**

**Summary of Changes**

This release introduces two key updates to improve the changelog generation process and enhance the security of the CI pipeline.

**Detailed Changes**

1. **Changelog Generation Update**: The `generate_changelog.py` script has been modified to overwrite the changelog file instead of appending to it. This change ensures that the changelog remains up-to-date and accurate, reflecting the latest changes in the repository.
2. **CI Pipeline Security Enhancement**: A personal access token has been added to the CI pipeline configuration in `.github/workflows/ci_pipeline.yml`. This addition enhances the security of the pipeline by providing a secure way to authenticate and authorize access to repository resources.

**Affected Files**

* `.github/scripts/generate_changelog.py`: Updated to overwrite the changelog file.
* `.github/workflows/ci_pipeline.yml`: Modified to include a personal access token for enhanced security.

**Impact and Benefits**

These changes aim to improve the overall efficiency and security of the development workflow. The updated changelog generation process ensures that the changelog remains accurate and easy to maintain, while the addition of a personal access token to the CI pipeline enhances the security and integrity of the pipeline.
