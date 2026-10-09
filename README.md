# IDA Assist sessions

Static HTML session exports, published automatically with GitHub Pages.

- Site: https://19h.github.io/assist-sessions/
- Repository: https://github.com/19h/assist-sessions
- First session: https://19h.github.io/assist-sessions/session-8198c5f1.html

The repository and deployed session contents are public.

## Publish a session

Put the exported HTML file in `sessions/`, commit it, and push to `main`:

```sh
cd /Users/int/dev/assist-sessions
cp /path/to/session-next.html sessions/
git add -- sessions/session-next.html
git commit -m "Publish session-next"
git push
```

The deployment workflow regenerates the index and publishes the site. A file
named `sessions/session-next.html` is available at
`https://19h.github.io/assist-sessions/session-next.html` after deployment.

You can also upload files directly into `sessions/` using GitHub's web UI.
Commit to `main` to deploy, or merge a pull request into `main`.

Nested directories and relative assets are preserved. For example,
`sessions/example/session.html` becomes `/assist-sessions/example/session.html`.
Keep any referenced images, stylesheets, and scripts at their corresponding
relative paths inside `sessions/`. The root name `sessions/index.html` is
reserved for the generated index. Symbolic links are rejected.

## Preview locally

Python 3.10 or newer is sufficient; there are no third-party dependencies.

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Open http://localhost:8000/ and stop the server with Ctrl-C.

## Deployment

The workflow in `.github/workflows/pages.yml` runs when session files, the
builder, or the workflow change on `main`. It can also be run manually from
GitHub Actions. Pages uses the **GitHub Actions** publishing source.

```text
sessions/ -> generated _site/ + index.html -> GitHub Pages
```

HTML exports are copied byte-for-byte. Only the index is generated: titles and
paths are HTML-escaped and link paths are URL-encoded. Removing a source file
removes it from the next deployment; Git history still retains committed files.

The builder takes O(B + N log N) time for B input bytes and N source paths. It
uses O(H + N + I) memory for the largest HTML file H, path list N, and generated
index I; the output occupies O(B + I) disk space.

GitHub's [custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
describes the deployment mechanism.
