#!/usr/bin/env node
import meow from 'meow';

meow(`
  Usage
    $ clou <command> [options]

  Commands
    chat     Start an interactive chat session
    session  Manage sessions
    search   Search conversations
    config   Manage configuration

  Options
    --help     Show help
    --version  Show version

  Examples
    $ clou chat
    $ clou session list
    $ clou search "query"
`, {
  importMeta: import.meta,
  flags: {
    version: {
      type: 'boolean',
      shortFlag: 'v',
    },
  },
});

console.log('Clouseau CLI - LLM Interaction Inspector');
