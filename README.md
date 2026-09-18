# DSA Revision Bible

The pattern library, retention system and Java combat reference as a fast, searchable website. The content lives in plain Markdown files, and GitHub rebuilds and publishes the site every time you commit a change.

## Put it online (one time, about five minutes)

1. On GitHub, create a new **empty** repository called `dsa-revision-bible`. Don't add a README, .gitignore or licence.
2. Unzip this folder, open a terminal inside it and push it:

   ```bash
   git init
   git add .
   git commit -m "DSA Revision Bible"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/dsa-revision-bible.git
   git push -u origin main
   ```

   With the GitHub CLI, `gh repo create dsa-revision-bible --public --source . --push` does the same in one line.
3. In the repository, open **Settings → Pages**. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Open the **Actions** tab and select **Build and deploy site**. If the first run failed because Pages wasn't switched on yet, press **Re-run all jobs**; otherwise press **Run workflow**. It takes about a minute.
5. Your site is at `https://YOUR-USERNAME.github.io/dsa-revision-bible/`. Bookmark it, or use **Add to Home screen** on your phone.

A GitHub Pages site is public to anyone who has the address, even when the repository is private. Pages from a private repository needs GitHub Pro, which is free with the GitHub Student Developer Pack.

## Edit, add or remove content

Every page has three buttons at the bottom:

- **Edit this page** opens that page's Markdown file in GitHub's editor.
- **Add a page to this part** opens a new file, already filled in with a starter template, in the right folder.
- **Delete this page** removes that page's file.

Commit the change and the site updates about a minute later. The build time and commit are shown at the foot of every page, so you can tell when your change is live.

The format is ordinary Markdown with a few additions (callouts, template blocks, verdict colours). **[EDITING.md](EDITING.md)** covers all of it, including how to add a new pattern card or a whole new Part.

## Preview on your own computer (optional)

```bash
pip install -r requirements.txt
python build/build.py            # writes dist/index.html; open it in your browser
python build/build.py --watch    # rebuilds on every save; just refresh the browser
```

The build prints a warning for anything it couldn't resolve, such as a link to a section that doesn't exist. The same warnings appear in the Actions log on GitHub.

## What's in here

```
content/            the Bible itself: one Markdown file per page, one folder per Part
  _home.md          the home page
  2-patterns/       e.g. Part II; _part.md holds the Part's name, tab and colour
build/              the site generator (Python) plus the page's CSS and JavaScript
.github/workflows/  builds and publishes the site on every push to main
```

## Your anchor log

The **Log today** buttons (on each card and in Appendix C) save to the browser you're using. To carry the log to another device, go to **Appendix C** and use **Export log** on one device and **Import log** on the other. Importing merges the logs, so nothing is lost.

## Keyboard

| Key | Action |
| --- | --- |
| `Ctrl K` or `/` | Search. You can also type a jump such as `7.3`, `card 10`, `g6`, `10b` or `app c` |
| `[` and `]` | Previous and next page |
| `C` | Cover templates, so you can blank-page them before revealing |
