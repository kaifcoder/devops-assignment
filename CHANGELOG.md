
## Latest Changes
## Changelog

### Release Summary

This release introduces significant improvements to the auto-merge workflow, enhancing its functionality, clarity, and efficiency. The changes aim to simplify the workflow, reduce unnecessary steps, and improve the overall user experience.

### Key Changes

1. **Simplified Auto-Merge Workflow**: The auto-merge workflow has been refactored to simplify trigger conditions for Dependabot PRs, making it more efficient and easier to maintain.
2. **Restrict Auto-Merge to Main Branch**: The auto-merge workflow is now restricted to pull requests targeting the main branch, ensuring that auto-merges only occur on the primary branch.
3. **Improved Code Review Script**: The code review script has been updated to ignore changes in YAML files and specify markdown format for generated review output, enhancing the review process.
4. **Enhanced Test Messages**: The `test_automerge` message has been updated for clarity and to reflect version 3, providing more accurate and informative test results.
5. **Workflow Renaming**: The auto-merge workflow has been renamed for clarity, improving the overall readability and understanding of the workflow.
6. **Removed Unnecessary Rebase Option**: The unnecessary rebase option has been removed from the auto-merge command, streamlining the workflow and reducing potential errors.
7. **Added Auto-Merge and Branch Deletion Steps**: Auto-merge and branch deletion steps have been added to the workflow, providing a more comprehensive and automated process.

### Technical Changes

* The `.github/workflows/auto_merge.yml` file has been updated with 8 insertions and 3 deletions, reflecting the changes made to the auto-merge workflow.

### Upgrade Notes

This release is a significant improvement to the auto-merge workflow, and users are encouraged to upgrade to take advantage of the new features and improvements. Please review the updated workflow and code review script to ensure a smooth transition.
