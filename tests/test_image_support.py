"""
tests/test_image_support.py

Test suite for image support in md_parser.py.
Covers:
  - _safe_image_src(): URL scheme validation
  - _inline_formatting(): inline image syntax
  - _markdown_to_html(): block image syntax
  - parse_markdown_to_slides(): regression — no images, existing features
  - Normal link handling not affected by image changes
"""

import pytest
import sys
import os

# Ensure md_parser is importable from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from md_parser import (
    parse_markdown_to_slides,
    _markdown_to_html,
    _inline_formatting,
    _safe_image_src,
)


# ─────────────────────────────────────────────────────────────────────────────
# _safe_image_src tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSafeImageSrc:
    def test_https_url_returned_unchanged(self):
        # Arrange
        url = "https://example.com/image.png"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == url

    def test_http_url_returned_unchanged(self):
        # Arrange
        url = "http://example.com/image.jpg"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == url

    def test_javascript_scheme_blocked(self):
        # Arrange
        url = "javascript:alert(1)"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_data_scheme_blocked(self):
        # Arrange
        url = "data:text/html,<script>alert(1)</script>"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_vbscript_scheme_blocked(self):
        # Arrange
        url = "vbscript:MsgBox(1)"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_empty_url_returned_as_empty_string(self):
        # Arrange
        url = ""

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_relative_url_blocked(self):
        # Arrange — les chemins relatifs n'ont pas de scheme http/https explicite
        url = "/images/photo.png"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_file_scheme_blocked(self):
        # Arrange — file:// pourrait lire le filesystem du serveur via Playwright
        url = "file:///etc/passwd"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""

    def test_url_with_spaces_encoded(self):
        # Arrange
        url = "https://example.com/my image.png"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == "https://example.com/my%20image.png"

    def test_javascript_scheme_case_insensitive(self):
        # Arrange
        url = "JAVASCRIPT:alert(1)"

        # Act
        result = _safe_image_src(url)

        # Assert
        assert result == ""


# ─────────────────────────────────────────────────────────────────────────────
# _inline_formatting — inline image tests
# ─────────────────────────────────────────────────────────────────────────────

class TestInlineImages:
    def test_inline_image_has_correct_class(self):
        # Arrange
        md = "![Mon Alt](https://example.com/img.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert 'class="slide-image slide-image-inline"' in result

    def test_inline_image_has_correct_src(self):
        # Arrange
        md = "![Mon Alt](https://example.com/img.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert 'src="https://example.com/img.png"' in result

    def test_inline_image_has_correct_alt(self):
        # Arrange
        md = "![Mon Alt](https://example.com/img.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert 'alt="Mon Alt"' in result

    def test_inline_image_empty_alt(self):
        # Arrange
        md = "![](https://example.com/img.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert 'alt=""' in result

    def test_inline_image_javascript_scheme_renders_text_fallback(self):
        # Arrange
        md = "![alt](javascript:alert(1))"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert "[image: alt]" in result
        assert "<img" not in result

    def test_inline_image_data_scheme_renders_text_fallback(self):
        # Arrange
        md = "![alt](data:text/html,foo)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert "[image: alt]" in result
        assert "<img" not in result

    def test_normal_link_not_converted_to_image(self):
        # Arrange
        md = "[texte](https://x.com)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert "<img" not in result
        assert '<a href="https://x.com"' in result

    def test_image_syntax_processed_before_link_syntax(self):
        # Arrange — an image followed by a link on the same text
        md = "![img alt](https://example.com/a.png) and [link text](https://example.com)"

        # Act
        result = _inline_formatting(md)

        # Assert — image becomes <img>, link becomes <a>
        assert "slide-image-inline" in result
        assert "<a " in result
        # Ensure the image alt is NOT accidentally treated as link text
        assert "img alt</a>" not in result

    def test_inline_image_has_onerror_handler(self):
        # Arrange
        md = "![alt](https://example.com/img.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert "onerror=" in result


# ─────────────────────────────────────────────────────────────────────────────
# _markdown_to_html — block image tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBlockImages:
    def test_block_image_wraps_in_figure(self):
        # Arrange
        md = "![Mon image](https://x.com/a.jpg)"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert '<figure class="slide-figure">' in result

    def test_block_image_with_alt_has_figcaption(self):
        # Arrange
        md = "![Mon image](https://x.com/a.jpg)"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert '<figcaption class="slide-image-credit">Mon image</figcaption>' in result

    def test_block_image_empty_alt_no_figcaption(self):
        # Arrange
        md = "![](https://x.com/a.jpg)"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "<figcaption" not in result

    def test_block_image_invalid_scheme_produces_no_figure(self):
        # Arrange
        md = "![alt](javascript:alert(1))"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "<figure" not in result
        assert "<img" not in result

    def test_block_image_invalid_scheme_produces_no_img(self):
        # Arrange
        md = "![alt](data:text/html,bad)"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "<img" not in result

    def test_block_image_has_onerror_handler(self):
        # Arrange
        md = "![alt](https://example.com/photo.png)"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "onerror=" in result

    def test_inline_image_in_paragraph_has_onerror_handler(self):
        # Arrange — image embedded in surrounding text (inline context)
        md = "Some text with ![alt](https://example.com/photo.png) inside."

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "onerror=" in result
        assert "slide-image-inline" in result


# ─────────────────────────────────────────────────────────────────────────────
# Regression tests — backward compatibility (no images)
# ─────────────────────────────────────────────────────────────────────────────

class TestNoImageRegression:
    def test_plain_text_body_no_figure_no_image(self):
        # Arrange
        md = "Just plain text without any images."

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "<figure" not in result
        assert "slide-image" not in result

    def test_bullet_list_renders_correctly(self):
        # Arrange
        md = "- Item one\n- Item two\n- Item three"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert '<ul class="bullets">' in result
        assert "slide-image" not in result

    def test_markdown_table_renders_correctly(self):
        # Arrange
        md = "| Col A | Col B |\n|-------|-------|\n| 1     | 2     |"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert '<table class="slide-table">' in result

    def test_blockquote_renders_correctly(self):
        # Arrange
        md = "> This is a blockquote"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert '<blockquote class="slide-quote">' in result

    def test_code_block_renders_correctly(self):
        # Arrange
        md = "```python\nprint('hello')\n```"

        # Act
        result = _markdown_to_html(md)

        # Assert
        assert "<pre" in result

    def test_parse_markdown_to_slides_without_images_returns_valid_structure(self):
        # Arrange
        md = """\
---
series: "Test Series"
author: "@tester"
---

# Introduction

This is a simple slide without any images.

## Second Slide

More content here.
"""

        # Act
        result = parse_markdown_to_slides(md)

        # Assert
        assert "slides" in result
        assert "footer" in result
        assert isinstance(result["slides"], list)
        assert len(result["slides"]) > 0
        # No image artifacts
        for slide in result["slides"]:
            body = slide.get("body", "")
            assert "<figure" not in body
            assert "slide-image" not in body

    def test_parse_markdown_no_images_no_exception(self):
        # Arrange
        md = "## Simple Slide\n\nSome content here."

        # Act & Assert (must not raise)
        result = parse_markdown_to_slides(md)
        assert result is not None


# ─────────────────────────────────────────────────────────────────────────────
# Normal links — not affected by image changes
# ─────────────────────────────────────────────────────────────────────────────

class TestLinksUnaffected:
    def test_normal_link_renders_as_anchor(self):
        # Arrange
        md = "[cliquez ici](https://example.com)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert '<a href="https://example.com"' in result
        assert "cliquez ici" in result
        assert "<img" not in result

    def test_javascript_link_href_blocked_to_hash(self):
        # Arrange
        md = "[click me](javascript:alert(1))"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert 'href="#"' in result
        assert "javascript:" not in result

    def test_link_text_does_not_get_treated_as_image(self):
        # Arrange — a link that has no ! prefix must NOT become an <img>
        md = "[not an image](https://example.com/image.png)"

        # Act
        result = _inline_formatting(md)

        # Assert
        assert "<img" not in result
        assert "<a " in result
