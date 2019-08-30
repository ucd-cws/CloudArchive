# CloudBackup
Projects no longer live on the file server - they live scattered across many cloud services,
but often also on the fileserver. This project aims to build a system that ensures that

1. cloud data and code repositories are discoverable by staff and
2. that copies of those repositories make their way to the fileserver for archival, access, and safekeeping

The initial code is focused on GitHub repositories associated with projects. It will
run automated, scheduled backups from GitHub organizations, but will try to be smart
about which ones to back up. It will:

1. find all existing git repos on the file server, and determine their origin repository and project
2. find, from formatted files that staff maintain, a list of repositories associated with projects, but which haven't
been downloaded necessarily.
3. determine which ones already have copies, and how fresh those copies are
4. Make archives of all items without copies and all non-fresh copies (for a currently undetermined definition of freshness)
5. Make archives of all other items in the GitHub organization that weren't handled above
6. Write back to the formatted file in the cloud folder any remote origin references that
were found in the project folder but weren't included. We'll want to make sure it only does so for code that is ours -
could be via a list of organizations, or something else.

More to come - this code is in the early stages.