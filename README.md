# Bcast
This is a Python app that will handle broadcasting a message across multiple social media platforms (Mastodon, etc.)

It's intended use is to broadcast a "going live" message for streaming, but you can use it for pretty much anything that needs to be sent out across mutiple channels.


## Notes

### Templates
- Templates are JSON files that describe *where and what* will be posted. Customize one in the `template_samples` directory. Templates describe the channels to use by pointing to the file paths of channel config files.
  - `name` and `description` are not required and are just helpful notes.
  - `channels` are paths to the particular channels you want to send the message out to, by their config file. (Hint: multiple of the same service can be provided, given unique config files.)
  - `variables` will replace text in `{{var}}` markup. Can be treated as defaults and overriden on the command line with `--var`.
  - `media_path` will attach media (if the channel supports it) to the post. Optional.
  - `message` is the actual message to post; use `\n` for newlines, and variable names are in `{{var}}` format; use `{{!var}}` before the name if it's required to be present, otherwise vars are optional.

### Configs

- Config files are JSON files describing the required credentials for the various channels (services). Customize one in the `config_samples` directory.
- Each config file is unqiue to the service. See the example files for what data is required.

### Variable voerride

Variables can be provided inside the template, or provided via the command line with the `-v` / `--var` option. Multiple can be provided. Variables on the command line override template variable defaults.

## Example usage

`./broadcast.py templates/stream.json -o game="Blaster Master"`


## Selfish-ware

This documentation, and indeed, the app itself, are still a work in progress. This is a personal project intended for myself, so I will essentially be doing just enough work to satisfy my needs.

That said, I won't scoff at a PR implementing a new channel.

I can't control what you do with this, of course, but I will not be accepting or supporting channel implementations for Twitter/X, or other fascism-friendly platforms. You'll have to do that work yourself.