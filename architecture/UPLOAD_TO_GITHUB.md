# Add architecture/ to the existing AI Systems Architecture repository

1. Download and extract `observatory-architecture-github-upload.zip` on your Mac.
2. Open your existing **AI Systems Architecture** repository on GitHub.
3. Select **Add file → Upload files** from the repository's **Code** page.
4. Drag the **entire extracted `architecture` folder** into the upload area, not the outer ZIP and not just the four Markdown files.
5. Check that the file paths start with `architecture/` and that the existing `engine-archive/` and `framework/` folders are not overwritten.
6. Commit with a message such as: `Add ZPP architecture records and open validation index`.

The package **does not include a repository-root README**. Your current root README can be updated as a separate final step to link to `architecture/`, `framework/`, and `engine-archive/`.

## Integrity check (optional)

On Mac Terminal, from inside the extracted `architecture` folder:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

All entries should report `OK`.
