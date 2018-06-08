# coding=utf-8
import ConfigParser
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from commands import add

import main

class TestPost(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def integration_test_post(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        add.setTokenValue('SalamiArmy/InfoBoet', keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN'))
        newRequestObject = main.GithubWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.body = '''{
  "ref": "refs/heads/master",
  "before": "0ddab4e511aa0e361ad58ad92319b4c22baad7a5",
  "after": "aeb0dc3deae21220b9c452302bb7742e2f04c9fc",
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "compare": "https://github.com/SalamiArmy/InfoBoet/compare/0ddab4e511aa...aeb0dc3deae2",
  "commits": [
    {
      "id": "aeb0dc3deae21220b9c452302bb7742e2f04c9fc",
      "tree_id": "ae1c0242a70e384d80641dc868de943a0fcb5044",
      "distinct": true,
      "message": "catch this error",
      "timestamp": "2018-05-11T19:35:56+02:00",
      "url": "https://github.com/SalamiArmy/InfoBoet/commit/aeb0dc3deae21220b9c452302bb7742e2f04c9fc",
      "author": {
        "name": "Ashley Lewis",
        "email": "ultrakiff@gmail.com",
        "username": "SalamiArmy"
      },
      "committer": {
        "name": "GitHub",
        "email": "noreply@github.com",
        "username": "web-flow"
      },
      "added": [

      ],
      "removed": [

      ],
      "modified": [
        "telegram_commands/getsuggestion.py"
      ]
    }
  ],
  "head_commit": {
    "id": "aeb0dc3deae21220b9c452302bb7742e2f04c9fc",
    "tree_id": "ae1c0242a70e384d80641dc868de943a0fcb5044",
    "distinct": true,
    "message": "catch this error",
    "timestamp": "2018-05-11T19:35:56+02:00",
    "url": "https://github.com/SalamiArmy/InfoBoet/commit/aeb0dc3deae21220b9c452302bb7742e2f04c9fc",
    "author": {
      "name": "Ashley Lewis",
      "email": "ultrakiff@gmail.com",
      "username": "SalamiArmy"
    },
    "committer": {
      "name": "GitHub",
      "email": "noreply@github.com",
      "username": "web-flow"
    },
    "added": [

    ],
    "removed": [

    ],
    "modified": [
      "telegram_commands/getsuggestion.py"
    ]
  },
  "repository": {
    "id": 91012547,
    "name": "InfoBoet",
    "full_name": "SalamiArmy/InfoBoet",
    "owner": {
      "name": "SalamiArmy",
      "email": "ultrakiff@gmail.com",
      "login": "SalamiArmy",
      "id": 8664897,
      "avatar_url": "https://avatars2.githubusercontent.com/u/8664897?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/SalamiArmy",
      "html_url": "https://github.com/SalamiArmy",
      "followers_url": "https://api.github.com/users/SalamiArmy/followers",
      "following_url": "https://api.github.com/users/SalamiArmy/following{/other_user}",
      "gists_url": "https://api.github.com/users/SalamiArmy/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/SalamiArmy/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/SalamiArmy/subscriptions",
      "organizations_url": "https://api.github.com/users/SalamiArmy/orgs",
      "repos_url": "https://api.github.com/users/SalamiArmy/repos",
      "events_url": "https://api.github.com/users/SalamiArmy/events{/privacy}",
      "received_events_url": "https://api.github.com/users/SalamiArmy/received_events",
      "type": "User",
      "site_admin": false
    },
    "private": false,
    "html_url": "https://github.com/SalamiArmy/InfoBoet",
    "description": "Intelligent Chat Bot",
    "fork": false,
    "url": "https://github.com/SalamiArmy/InfoBoet",
    "forks_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/forks",
    "keys_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/teams",
    "hooks_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/hooks",
    "issue_events_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/issues/events{/number}",
    "events_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/events",
    "assignees_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/assignees{/user}",
    "branches_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/branches{/branch}",
    "tags_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/tags",
    "blobs_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/languages",
    "stargazers_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/stargazers",
    "contributors_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/contributors",
    "subscribers_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/subscribers",
    "subscription_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/subscription",
    "commits_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/contents/{+path}",
    "compare_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/merges",
    "archive_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/downloads",
    "issues_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/issues{/number}",
    "pulls_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/labels{/name}",
    "releases_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/releases{/id}",
    "deployments_url": "https://api.github.com/repos/SalamiArmy/InfoBoet/deployments",
    "created_at": 1494528238,
    "updated_at": "2018-05-11T13:46:03Z",
    "pushed_at": 1526060156,
    "git_url": "git://github.com/SalamiArmy/InfoBoet.git",
    "ssh_url": "git@github.com:SalamiArmy/InfoBoet.git",
    "clone_url": "https://github.com/SalamiArmy/InfoBoet.git",
    "svn_url": "https://github.com/SalamiArmy/InfoBoet",
    "homepage": null,
    "size": 225,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "Python",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 1,
    "mirror_url": null,
    "archived": false,
    "open_issues_count": 1,
    "license": {
      "key": "other",
      "name": "Other",
      "spdx_id": null,
      "url": null
    },
    "forks": 1,
    "open_issues": 1,
    "watchers": 0,
    "default_branch": "master",
    "stargazers": 0,
    "master_branch": "master"
  },
  "pusher": {
    "name": "SalamiArmy",
    "email": "ultrakiff@gmail.com"
  },
  "sender": {
    "login": "SalamiArmy",
    "id": 8664897,
    "avatar_url": "https://avatars2.githubusercontent.com/u/8664897?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/SalamiArmy",
    "html_url": "https://github.com/SalamiArmy",
    "followers_url": "https://api.github.com/users/SalamiArmy/followers",
    "following_url": "https://api.github.com/users/SalamiArmy/following{/other_user}",
    "gists_url": "https://api.github.com/users/SalamiArmy/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/SalamiArmy/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/SalamiArmy/subscriptions",
    "organizations_url": "https://api.github.com/users/SalamiArmy/orgs",
    "repos_url": "https://api.github.com/users/SalamiArmy/repos",
    "events_url": "https://api.github.com/users/SalamiArmy/events{/privacy}",
    "received_events_url": "https://api.github.com/users/SalamiArmy/received_events",
    "type": "User",
    "site_admin": false
  }
}'''
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()
