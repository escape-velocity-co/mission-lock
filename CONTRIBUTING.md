# Contributing

Documentation for the repository is present in [CLAUDE.md](CLAUDE.md). That's typically created by an LLM but in this case was artisanally crafted, single-origin text, so hopefully human-readable.

## Ways to Contribute

We are continuing to iterate on a standard that MLA can assess, in whole or in part. That standard is expressed in the [Attributes](skills/mission-lock/definitions/attributes.md) and [Rules](skills/mission-lock/definitions/rules.md) definitions in the skill.

Where we could really use help are the following:

* **Testing against additional charters**: The eval corpus is mostly Delaware public-company charters, and those charters tend to be materially tidied up before going public. Texas and Nevada are on the rise as states of incorporation, of particular relevance to *Incorruptible* because of their attempts to reduce short-term pressure and activist-investor risk for founders. We'd like this skill to be useful to every company, so the more charters it can be tested against, the better. Here are some options if you'd like to contribute:
  * **[Request](https://github.com/escape-velocity-co/mission-lock/issues/new?template=charter-submission.yml) to add your charter to the corpus**: I'll have a look and see if it exercises something the corpus doesn't cover yet. *The corpus is public, as are charters, but if you're not comfortable with that, don't submit it.*
  * **Live feedback session**: Schedule a call with me (`rob at escapevelocity dot co`). If you've got a charter you'd like to go through together and I've got room, it would be great to connect.

* **Report an unexpected analysis**: If MLA understood things unclearly or incorrectly, please [open an issue](https://github.com/escape-velocity-co/mission-lock/issues/new?template=unexpected-analysis.yml).

* **Improve analysis accuracy of the Attributes or Rules**: The corpus consists of as many positive and negative tests cases are required to fully exercise each Attribute and Rule, though it's certainly possible cases have been missed! Please open an [issue](https://github.com/escape-velocity-co/mission-lock/issues) should you discover one.

## Licensing

MLA is licensed under the [MPL-2.0](LICENSE). By contributing, you agree that your contribution is licensed under the same terms.
