{{/*
  Markdown rendering of the front page.

  Hextra ships page.markdown.md, section.markdown.md, wide.markdown.md and
  glossary.markdown.md, and no template for the home kind. Hugo therefore wrote
  nothing for home + markdown while the page context menu went on rendering
  "Copy as Markdown" and "View as Markdown" pointing at /index.md, which 404ed.
  Broken on the one page most people land on, and on the one page most worth
  handing to an assistant, since the front page is the whole quickstart.

  On Hextra's own site the home page is a landing page with no prose, so the
  gap costs them nothing and would not have been noticed there.

  Deliberately identical to the theme's other two rather than improved on: a
  divergence here would show up as the front page formatting differently from
  every section, which is the sort of difference nobody attributes to a
  template override six months later.
*/ -}}
{{- .Title | replaceRE "\n" " " | printf "# %s" }}
{{ .RawContent }}
