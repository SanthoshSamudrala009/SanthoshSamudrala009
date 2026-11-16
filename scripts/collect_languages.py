"""Fetch a private allowlist into an ignored candidate; never publish automatically."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request

from render_profile import ROOT, exact_keys, validate


class RefreshError(Exception):
    """A deliberately privacy-safe diagnostic, without API payloads or repo names."""


def normalize(value):
    return re.sub(r'[^a-z0-9]', '', value.casefold())


def selected_repositories(config):
    exact_keys(config, ('owner', 'repositories', 'exclude'), 'private configuration')
    if not isinstance(config['owner'], str) or not re.fullmatch(r'[A-Za-z0-9-]{1,39}', config['owner']):
        raise RefreshError('configuration: invalid owner')
    repos, exclude = config['repositories'], config['exclude']
    if not isinstance(repos, list) or not 1 <= len(repos) <= 100:
        raise RefreshError('configuration: expected 1 to 100 explicit repository names')
    if not isinstance(exclude, list) or not exclude or any(not isinstance(x, str) or not normalize(x) for x in exclude):
        raise RefreshError('configuration: an explicit nonempty exclusion list is required')
    if any(not isinstance(r, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', r) or r in ('.', '..') for r in repos):
        raise RefreshError('configuration: invalid repository name')
    if len({r.casefold() for r in repos}) != len(repos):
        raise RefreshError('configuration: duplicate repositories would inflate totals')
    blocked = [normalize(x) for x in exclude]
    return [r for r in repos if not any(x in normalize(r) for x in blocked)]


def github_token(owner):
    token = os.environ.get('PROFILE_READ_TOKEN')
    if token:
        return token
    env = dict(os.environ, GCM_INTERACTIVE='Never', GIT_TERMINAL_PROMPT='0')
    try:
        result = subprocess.run(['git', 'credential', 'fill'],
                                input=f'protocol=https\nhost=github.com\nusername={owner}\n\n',
                                text=True, capture_output=True, env=env, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise RefreshError('authentication: credential helper unavailable') from None
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if result.returncode or not fields.get('password'):
        raise RefreshError('authentication: sign in to Git Credential Manager first')
    return fields['password']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RefreshError('fetch: redirected repository; review the local allowlist')


def api_client(token):
    opener = urllib.request.build_opener(NoRedirect())

    def get(path):
        request = urllib.request.Request('https://api.github.com' + path, headers={
            'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
            'User-Agent': 'Midnight-Workshop-Language-Refresh',
        })
        try:
            with opener.open(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            raise RefreshError(f'fetch: GitHub HTTP {exc.code}; candidate unchanged') from None
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            raise RefreshError('fetch: network or response error; candidate unchanged') from None

    return get


def collect(current, config, get, snapshot_date):
    validate(current)
    names = selected_repositories(config)
    if current['handle'].casefold() != config['owner'].casefold():
        raise RefreshError('configuration: snapshot handle differs from repository owner')
    counts = Counter()
    used = 0
    for name in names:
        path = '/repos/' + config['owner'] + '/' + name
        repo = get(path)
        if not isinstance(repo, dict) or any(k not in repo for k in ('private', 'fork', 'archived', 'owner', 'name')):
            raise RefreshError('metadata: incomplete repository response')
        if any(type(repo[k]) is not bool for k in ('private', 'fork', 'archived')):
            raise RefreshError('metadata: invalid repository flags')
        if not isinstance(repo['owner'], dict) or str(repo['owner'].get('login', '')).casefold() != config['owner'].casefold() or str(repo['name']).casefold() != name.casefold():
            raise RefreshError('metadata: repository identity changed; review local allowlist')
        if not repo['private'] or repo['fork'] or repo['archived']:
            continue
        languages = get(path + '/languages')
        if not isinstance(languages, dict):
            raise RefreshError('languages: invalid response')
        if any(not isinstance(k, str) or type(v) is not int or v <= 0 or v > 10**13 for k, v in languages.items()):
            raise RefreshError('languages: invalid byte counts')
        if languages:
            used += 1
            counts.update(languages)
    if not used:
        raise RefreshError('languages: no eligible language data; candidate unchanged')
    candidate = json.loads(json.dumps(current))
    candidate['snapshot'] = {'date': snapshot_date, 'repository_count': used, 'languages': dict(sorted(counts.items()))}
    validate(candidate)
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'profile.private.json')
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding='utf-8'))
        selected_repositories(config)
        current = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
        validate(current)
        token = github_token(config['owner'])
        candidate = collect(current, config, api_client(token), datetime.now(timezone.utc).date().isoformat())
        target = ROOT / '.preview-cache' / 'profile.candidate.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_suffix('.tmp')
        temp.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
        os.replace(temp, target)
    except RefreshError as exc:
        sys.exit(str(exc))
    except (OSError, ValueError, TypeError, KeyError):
        sys.exit('configuration or output: invalid input or file error; public snapshot unchanged')
    print(f"Candidate ready: {candidate['snapshot']['repository_count']} repositories. Public snapshot unchanged.")
    print('Review .preview-cache/profile.candidate.json before copying it to profile.json and rendering.')


if __name__ == '__main__':
    main()
