---
description: Process a downloaded .eml email file and create a blog post. Extracts subject, date, body text, and images. Triggered by /process-email.
argument-hint: [path-to-eml-file]
disable-model-invocation: true
allowed-tools: Bash Read Write Glob
---

You are processing a downloaded `.eml` email file to create a new blog post for a Jekyll website. Follow these steps in order.

## Step 1: Read and parse the .eml file

Read the file at the path provided by the user. An `.eml` file is a raw MIME email with headers and body.

Extract:
- **Subject**: Decode any RFC 2047 encoded-words (`=?UTF-8?B?...?=` or `=?UTF-8?Q?...?=`). Use Python's `email.header.decode_header()` via a quick inline Python snippet if needed.
- **Date**: The `Date` header. Parse it to `YYYY-MM-DD` format.
- **From**: The `From` header (informational only).
- **Body text**: Prefer the `text/plain` part. If none exists, convert the `text/html` part to Markdown using `html2text` (install with `pip install html2text` if not present). Strip email signatures, disclaimers, and forwarded message chains — keep only the actual post content.
- **Images**: Find all image parts (`image/jpeg`, `image/png`, `image/gif`, `image/webp`). These can be:
  - Inline (`Content-Disposition: inline` or referenced by `cid:` in the HTML)
  - Attachments (`Content-Disposition: attachment`)
  - Extract all of them. Decode their content-transfer-encoding (base64 or quoted-printable). Note the original filename from the part header or `Content-Type` name parameter.

Run the persistent `parse_email.py` script located alongside this SKILL.md:

```
python .claude/skills/process-email/parse_email.py <eml_path>
```

This outputs JSON with `subject`, `date`, `from`, `body`, `image_count`, and `image_names` fields.

## Step 2: Present preview to the user

Show the user what you extracted:

```
Subject:  "..."
Date:     YYYY-MM-DD (from email header)
From:     sender@example.com

Body preview (first ~500 chars):
  Lorem ipsum dolor sit amet...

Images found: N
  1. filename1.jpg (123 KB)
  2. filename2.png (456 KB)
```

## Step 3: Interactive confirmation

Use `AskUserQuestion` to confirm with the user:

**First question** — confirm the title, date, and slug:

Ask for:
- **Title**: default is the email subject, cleaned up (remove RE:, FWD:, extra whitespace)
- **Date**: default is the email's sent date in `YYYY-MM-DD` format
- **Slug**: auto-generated from the title (lowercase, replace spaces/illegal chars with hyphens, collapse multiple hyphens, strip leading/trailing hyphens, max ~60 chars)

If the user corrects anything, use their values.

**Second question** (only if images were found) — pick the teaser image:

Show each image filename and ask which should be the teaser. Options: "1", "2", "3", etc., plus "None (I'll add later)".

## Step 4: Clean up the body text

- If the body came from `text/plain`, keep it as-is but remove obvious email signatures (lines matching `-- `, `--\n`, `Sent from my`, `Get Outlook for`, etc.)
- If the body came from `text/html`, convert HTML to Markdown using Python's `html2text` library
- Normalize line endings and trim excess whitespace
- Present the cleaned body to the user and ask if they want to make any edits before proceeding. If they do, let them specify changes.

## Step 5: Save images

For each extracted image:
1. Sanitize the filename: replace spaces and special chars with hyphens, keep the extension
2. If the sanitized name is empty or just an extension, generate a name like `email-image-YYYYMMDD-N.jpg`
3. If a file with the same name already exists in `assets/images/news/`, append `-1`, `-2` etc. before the extension
4. Decode the base64 data and write the image to `assets/images/news/<sanitized-name>`
5. Track which image was chosen as the teaser

Run the persistent `save_images.py` script located alongside this SKILL.md:

```
python .claude/skills/process-email/save_images.py <eml_path> [output_dir]
```

This saves all images from the .eml to `assets/images/news/` (by default) with sanitized filenames and collision handling. It prints a JSON mapping of original names to saved paths.

## Step 6: Generate the post Markdown

Write the post to `_posts/YYYY-MM-DD-slug.md` using this exact format:

```markdown
---
title: "Confirmed Title"
layout: single
classes: wide
header:
  teaser: /assets/images/news/teaser-image-filename.jpg
categories:
  - News
---

Body text goes here. Each paragraph separated by blank lines.

{% include figure image_path="/assets/images/news/image1.jpg" %}

More body text if needed.

{% include figure image_path="/assets/images/news/image2.jpg" %}
```

Rules:
- The teaser line is omitted entirely if the user chose "None"
- Images appear in the body where they make sense contextually (intersperse with paragraphs)
- If the HTML body had images at specific positions (cid references), try to place them at those positions in the Markdown
- Use `{% include figure image_path="/assets/images/news/filename.jpg" %}` for every body image (NOT Markdown `![alt](path)` syntax)
- Image paths must start with `/assets/images/news/`
- Wrap the figure include on its own line with a blank line before and after

## Step 7: Final output

Print a summary:
- Post file path
- Images saved (count and paths)
- Teaser image used
- Remind the user they can run `bundle exec jekyll serve` to preview

## Edge cases

- **No plain text, no HTML body**: Warn the user that no body content was found
- **Email has no Date header**: Use today's date and flag it for the user
- **Subject is empty**: Use "Untitled" and let the user override
- **Image filename collision**: Auto-rename with numeric suffix
- **Very long emails**: Truncate the body preview in Step 2, but include all text in the final post
- **HTML-only email with cid images**: Match `cid:` references to extracted inline images and note the positions
- **win32 platform**: Use PowerShell for file operations where needed, or Python for cross-platform consistency
