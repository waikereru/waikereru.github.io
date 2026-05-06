import email
import email.header
import email.policy
import base64
import os
import re
import sys

def sanitize_filename(name):
    """Lowercase, replace spaces/special chars with hyphens, keep extension."""
    base, ext = os.path.splitext(name)
    base = base.lower().strip()
    base = re.sub(r'[^a-z0-9]+', '-', base)
    base = base.strip('-')
    if not base:
        base = 'email-image'
    return base + ext.lower()

def extract_and_save_images(eml_path, output_dir):
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

    saved = {}
    if not msg.is_multipart():
        return saved

    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type in ('image/jpeg', 'image/png', 'image/gif', 'image/webp'):
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            filename = part.get_filename()
            if filename:
                decoded = email.header.decode_header(filename)[0][0]
                if isinstance(decoded, bytes):
                    original_name = decoded.decode('utf-8', errors='replace')
                else:
                    original_name = decoded
            else:
                original_name = 'image.jpg'

            sanitized = sanitize_filename(original_name)

            # Handle collisions
            out_path = os.path.join(output_dir, sanitized)
            counter = 1
            base, ext = os.path.splitext(sanitized)
            while os.path.exists(out_path):
                new_name = f"{base}-{counter}{ext}"
                out_path = os.path.join(output_dir, new_name)
                counter += 1

            with open(out_path, 'wb') as f:
                f.write(payload)

            rel_path = os.path.join('/assets/images/news', os.path.basename(out_path))
            saved[original_name] = {
                'saved_as': os.path.basename(out_path),
                'path': rel_path.replace('\\', '/'),
                'size': len(payload)
            }
            print(f"Saved: {original_name} -> {os.path.basename(out_path)} ({len(payload):,} bytes)")

    return saved

if len(sys.argv) < 2:
    print("Usage: python save_images.py <eml_path> [output_dir]")
    print("  output_dir defaults to assets/images/news/ relative to project root")
    sys.exit(1)

eml_path = sys.argv[1]
if len(sys.argv) >= 3:
    output_dir = sys.argv[2]
else:
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'images', 'news')

saved = extract_and_save_images(eml_path, output_dir)

# Export mapping as JSON for later use
import json
print("\n---MAPPING---")
print(json.dumps(saved, indent=2))
