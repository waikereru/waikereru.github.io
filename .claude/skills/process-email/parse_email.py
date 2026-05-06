import email
import email.header
import email.policy
import base64
import quopri
import sys
import json

def decode_header_value(header_value):
    parts = email.header.decode_header(header_value)
    result = ''
    for part, charset in parts:
        if isinstance(part, bytes):
            result += part.decode(charset or 'utf-8', errors='replace')
        else:
            result += part
    return result

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disp = str(part.get('Content-Disposition', ''))
            if content_type == 'text/plain' and 'attachment' not in content_disp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return ('text/plain', payload.decode(charset, errors='replace'))
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disp = str(part.get('Content-Disposition', ''))
            if content_type == 'text/html' and 'attachment' not in content_disp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return ('text/html', payload.decode(charset, errors='replace'))
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            return (content_type, payload.decode(charset, errors='replace'))
    return ('none', '')

def extract_images(msg):
    images = []
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type in ('image/jpeg', 'image/png', 'image/gif', 'image/webp'):
                payload = part.get_payload(decode=True)
                if payload:
                    filename = part.get_filename()
                    if filename:
                        decoded = email.header.decode_header(filename)[0][0]
                        if isinstance(decoded, bytes):
                            filename = decoded.decode('utf-8', errors='replace')
                        else:
                            filename = decoded
                    images.append({
                        'filename': filename or 'image',
                        'content_type': content_type,
                        'data': base64.b64encode(payload).decode('ascii'),
                        'size': len(payload)
                    })
    return images

with open(sys.argv[1], 'rb') as f:
    msg = email.message_from_binary_file(f, policy=email.policy.default)

subject = decode_header_value(msg.get('Subject', 'Untitled'))
date = msg.get('Date', '')
from_addr = decode_header_value(msg.get('From', ''))
body_type, body = get_body(msg)
images = extract_images(msg)

print(json.dumps({
    'subject': subject,
    'date': date,
    'from': from_addr,
    'body_type': body_type,
    'body': body[:5000],
    'image_count': len(images),
    'image_names': [img['filename'] for img in images],
    'image_sizes': [img['size'] for img in images]
}, indent=2))
