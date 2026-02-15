#!/usr/bin/env python3
"""
Uploads the schedule image to Google Photos album.
Used by GitHub Actions after generating the updated schedule.
"""

import os
import sys
import requests


def get_access_token(client_id, client_secret, refresh_token):
    """Exchange refresh token for a fresh access token."""
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    })
    response.raise_for_status()
    return response.json()['access_token']


def upload_to_google_photos(image_path, access_token, album_id):
    """Upload an image to a Google Photos album."""

    # Step 1: Upload the image bytes and get an upload token
    with open(image_path, 'rb') as f:
        image_data = f.read()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': 'ramadan_schedule.png',
        'X-Goog-Upload-Protocol': 'raw',
    }
    upload_response = requests.post(
        'https://photoslibrary.googleapis.com/v1/uploads',
        headers=headers,
        data=image_data,
    )
    upload_response.raise_for_status()
    upload_token = upload_response.text
    print(f"Upload token received ({len(image_data)} bytes uploaded)")

    # Step 2: Create a media item in the album
    create_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    create_body = {
        'albumId': album_id,
        'newMediaItems': [{
            'description': f'Ramadan 1447 Schedule - Updated daily',
            'simpleMediaItem': {
                'uploadToken': upload_token,
                'fileName': 'ramadan_schedule.png',
            }
        }]
    }
    create_response = requests.post(
        'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
        headers=create_headers,
        json=create_body,
    )
    create_response.raise_for_status()
    result = create_response.json()

    status = result['newMediaItemResults'][0]['status']
    if status.get('message', '') == 'Success' or 'mediaItem' in result['newMediaItemResults'][0]:
        print("Successfully added to Google Photos album!")
    else:
        print(f"Upload status: {status}")

    return result


def main():
    # Read credentials from environment (set by GitHub Secrets)
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    refresh_token = os.environ.get('GOOGLE_REFRESH_TOKEN')
    album_id = os.environ.get('GOOGLE_PHOTOS_ALBUM_ID')

    if not all([client_id, client_secret, refresh_token, album_id]):
        print("ERROR: Missing Google credentials in environment variables.")
        print("Required: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, GOOGLE_PHOTOS_ALBUM_ID")
        sys.exit(1)

    image_path = 'docs/schedule.png'
    if not os.path.exists(image_path):
        print(f"ERROR: {image_path} not found. Run update_schedule.py first.")
        sys.exit(1)

    print("Getting access token...")
    access_token = get_access_token(client_id, client_secret, refresh_token)
    print("Access token obtained.")

    print(f"Uploading {image_path} to Google Photos...")
    upload_to_google_photos(image_path, access_token, album_id)
    print("Done!")


if __name__ == "__main__":
    main()
