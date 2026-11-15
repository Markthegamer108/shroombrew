# Shroombrew

Nintendo shut the Wii Shop Channel down in January 2019. Shroombrew is a fan-made server that brings it back.

You install a patched copy of the channel, and instead of trying to reach Nintendo it talks to this server. The website is at [shroombrew.org](https://shroombrew.org), where you can make Wii Points cards, look through every title and download the patched channel.

It's free. The Wii Points here aren't real money and nothing is for sale. This isn't affiliated with Nintendo in any way.

## What's in this repo

This branch (`main`) is the shop server. It's written in Go and started out as [WiiSOAP](https://github.com/OpenShopChannel/WiiSOAP). The website lives on the `gh-pages` branch.

Some folders worth knowing about:

- `shop/` has the pages, styles and scripts the shop shows, plus the checkout screens restored from the original channel
- `reference-site/` is a copy of wiishopchannel.net, used with permission
- `tools-src/` has the Homebrew Channel app that copies downloads onto your SD card
- `cmd/` and `tools/` are small helpers for building and patching channels

Older notes from while the server was being built are in [docs/dev-notes.md](docs/dev-notes.md).

## Where things are at

The patched channel is built for the original Wii. It still hasn't been tested on a real console, and vWii on a Wii U hasn't been tried at all, so back up your NAND before installing it.

Installing a title straight from the shop doesn't work yet. The server gets the download ready and the SD card app does the copying.

## Running it yourself

You'll need Go and PostgreSQL.

1. Copy `config.example.xml` to `config.xml` and fill it in.
2. Load `database.sql` into Postgres.
3. Put `catalog.json`, `icons/`, `site/` and `reference-site/` in the folder you run it from.
4. Run `go build .`, then start the binary. Set `SHROOMBREW_ADDR` if you want a different listen address.

Run the tests with `go test ./...`. If you have a throwaway database, `SHOP_INTEGRATION_CONFIG=/path/to/config.xml go test ./...` also runs the points and download tests against it.

If you only want to look at the browser version, `go run reference_site.go reference_preview.go -root reference-site` runs it without a database.

Behind a reverse proxy, make sure it sets `X-Forwarded-Proto`. And please don't commit your `config.xml`, keys, console credentials or NAND backups.

## Thanks

- Nathan Boehm / Comp Arison of [wiishopchannel.net](https://wiishopchannel.net/), for letting us use the frontend and pointing us to the [Wii Shop Channel HTML backup](https://archive.org/details/WiiShopChannelBackup)
- [Open Shop Channel](https://oscwii.org/) for the homebrew catalog
- [WiiSOAP](https://github.com/OpenShopChannel/WiiSOAP), which the server is built on

## License

AGPL-3.0-or-later, see `LICENSE`. Files copied from other projects keep their own notices. The server source can also be downloaded from the shop at `/source/shroombrew-source.tar.gz`.
