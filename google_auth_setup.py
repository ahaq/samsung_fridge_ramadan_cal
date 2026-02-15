#!/usr/bin/env python3
"""
ONE-TIME SETUP: Run this on your computer to authorize Google Photos access.
It will give you a refresh token to store in GitHub Secrets.

Prerequisites:
    pip install google-auth-oauthlib google-auth requests

Usage:
    python3 google_auth_setup.py
"""

import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary']

def main():
    print("=" * 60)
    print("Google Photos Authorization Setup")
    print("=" * 60)
    print()

    # Check if credentials file exists
    try:
        with open('google_credentials.json', 'r') as f:
            creds_data = json.load(f)
        print("Found google_credentials.json")
    except FileNotFoundError:
        print("ERROR: google_credentials.json not found!")
        print()
        print("Follow these steps first:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project (or select existing)")
        print("3. Enable 'Google Photos Library API'")
        print("4. Go to Credentials > Create Credentials > OAuth 2.0 Client ID")
        print("5. Application type: Desktop app")
        print("6. Download the JSON and save as 'google_credentials.json' here")
        return

    # Run OAuth flow
    print("Opening browser for authorization...")
    print()
    flow = InstalledAppFlow.from_client_secrets_file('google_credentials.json', SCOPES)
    credentials = flow.run_local_server(port=8080)

    print()
    print("=" * 60)
    print("SUCCESS! Here are your tokens.")
    print("=" * 60)
    print()
    print("Add these as GitHub Secrets in your repo")
    print("(Settings > Secrets and variables > Actions > New repository secret)")
    print()
    print(f"GOOGLE_CLIENT_ID:")
    print(f"  {credentials.client_id}")
    print()
    print(f"GOOGLE_CLIENT_SECRET:")
    print(f"  {credentials.client_secret}")
    print()
    print(f"GOOGLE_REFRESH_TOKEN:")
    print(f"  {credentials.refresh_token}")
    print()
    print("=" * 60)

    # Also create the album
    print()
    print("Now creating a 'Ramadan Schedule' album in Google Photos...")

    import requests
    headers = {
        'Authorization': f'Bearer {credentials.token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(
        'https://photoslibrary.googleapis.com/v1/albums',
        headers=headers,
        json={'album': {'title': 'Ramadan Schedule'}}
    )

    if response.status_code == 200:
        album = response.json()
        album_id = album['id']
        print(f"Album created! ID: {album_id}")
        print()
        print("Add this as another GitHub Secret:")
        print()
        print(f"GOOGLE_PHOTOS_ALBUM_ID:")
        print(f"  {album_id}")
        print()
        print("=" * 60)
        print("SUMMARY: Add these 4 secrets to GitHub:")
        print("  1. GOOGLE_CLIENT_ID")
        print("  2. GOOGLE_CLIENT_SECRET")
        print("  3. GOOGLE_REFRESH_TOKEN")
        print("  4. GOOGLE_PHOTOS_ALBUM_ID")
        print("=" * 60)
    else:
        print(f"Error creating album: {response.status_code}")
        print(response.text)
        print("You can create it manually in Google Photos and get the ID later.")


if __name__ == "__main__":
    main()
