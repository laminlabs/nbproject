# Changelog

<!-- prettier-ignore -->
Name | PR | User | Date | Patch
--- | --- | --- | --- | ---
Add an uninitialized project for `test_cli` and a small fix to `header` | [154](https://github.com/laminlabs/nbproject/pull/154) | [Koncopd](https://github.com/Koncopd) | 2022-07-13 | 0.2.2
🚸 Add extra safety measures, better documentation, better logging, and a separate test to avoid invalid notebook states | [153](https://github.com/laminlabs/nbproject/pull/153) | [falexwolf](https://github.com/falexwolf) | 2022-07-13 |
🚸 Clearer logging output upon init in VS Code and Classic Notebook | [152](https://github.com/laminlabs/nbproject/pull/152) | [falexwolf](https://github.com/falexwolf) | 2022-07-13 |
🔥 Remove automatically calling `header()` upon import | [151](https://github.com/laminlabs/nbproject/pull/151) | [falexwolf](https://github.com/falexwolf) | 2022-07-13 |
♻️ Enable passing the calling_code statement to publish | [148](https://github.com/laminlabs/nbproject/pull/148) | [falexwolf](https://github.com/falexwolf) | 2022-07-12 | 0.2.1
:sparkles: Add last cell check to publish | [143](https://github.com/laminlabs/nbproject/pull/143) | [Koncopd](https://github.com/Koncopd) | 2022-07-11 |
:memo: Add header() call to every notebook | [141](https://github.com/laminlabs/nbproject/pull/141) | [falexwolf](https://github.com/falexwolf) | 2022-07-11 | 0.2.0
🚸 Add `i_confirm_i_saved` arg to `publish()` for usage outside Jupyter Lab | [140](https://github.com/laminlabs/nbproject/pull/140) | [falexwolf](https://github.com/falexwolf) | 2022-07-11 |
🚚 Migrated test submodule to `nbproject_test` | [138](https://github.com/laminlabs/nbproject/pull/138) | [falexwolf](https://github.com/falexwolf) | 2022-07-11 |
🚚  Remove mention of footer, lock in publish | [137](https://github.com/laminlabs/nbproject/pull/137) | [falexwolf](https://github.com/falexwolf) | 2022-07-11 |
📝 Add a nutshell tutorial to demo canonical workflow | [135](https://github.com/laminlabs/nbproject/pull/135) | [falexwolf](https://github.com/falexwolf) | 2022-07-10 |
🚸 Turn `header()` from pseudo-module into function, remove `Header` class, keep auto-display upon import | [133](https://github.com/laminlabs/nbproject/pull/133) | [falexwolf](https://github.com/falexwolf) | 2022-07-10 |
:white_check_mark: Improve coverage | [130](https://github.com/laminlabs/nbproject/pull/130) | [Koncopd](https://github.com/Koncopd) | 2022-07-10 |
🚸  More intuitive API for updating dependency store and writing it to file | [126](https://github.com/laminlabs/nbproject/pull/126) | [falexwolf](https://github.com/falexwolf) | 2022-07-09 |
✨ Add a more convenient way of updating the dependency store | [125](https://github.com/laminlabs/nbproject/pull/125) | [Koncopd](https://github.com/Koncopd) | 2022-07-09 |
:lipstick: Prettify logging during testing | [124](https://github.com/laminlabs/nbproject/pull/124) | [falexwolf](https://github.com/falexwolf) | 2022-07-09 |
📝 Add a published notebook | [120](https://github.com/laminlabs/nbproject/pull/120) | [falexwolf](https://github.com/falexwolf) | 2022-07-05 |
✅ Improve notebook testing API | [116](https://github.com/laminlabs/nbproject/pull/116) | [Koncopd](https://github.com/Koncopd) | 2022-07-03 | 0.1.6
✨ Publish notebooks from the CLI | [112](https://github.com/laminlabs/nbproject/pull/112) | [Koncopd](https://github.com/Koncopd) | 2022-07-01 |
💄 Avoid non-JupyterLab env logging messages in CI env | [114](https://github.com/laminlabs/nbproject/pull/114) | [falexwolf](https://github.com/falexwolf) | 2022-07-01 | 0.1.5
✅ Execute notebooks in order of index | [113](https://github.com/laminlabs/nbproject/pull/113) | [falexwolf](https://github.com/falexwolf) | 2022-07-01 |
💄 More compact logging and other small fixes | [111](https://github.com/laminlabs/nbproject/pull/111) | [falexwolf](https://github.com/falexwolf) | 2022-07-01 | 0.1.4
♻️ Refactor meta and header | [110](https://github.com/laminlabs/nbproject/pull/110) | [Koncopd](https://github.com/Koncopd) | 2022-07-01 |
🚸 Polish publishing experience | [commit](https://github.com/laminlabs/nbproject/commit/dec15d05bcf3cdf17498fc1a164a29765d48a2e3) | [falexwolf](https://github.com/falexwolf) | 2022-07-01 | 0.1.3
🚸 Improve user experience during publishing | [109](https://github.com/laminlabs/nbproject/pull/109) | [falexwolf](https://github.com/falexwolf) | 2022-07-01 | 0.1.2
✨ Add VS Code integration | [107](https://github.com/laminlabs/nbproject/pull/107) | [falexwolf](https://github.com/falexwolf) | 2022-06-29 | 0.1.1
✨ Implement the publish function | [106](https://github.com/laminlabs/nbproject/pull/106) | [Koncopd](https://github.com/Koncopd) | 2022-06-29 |
📝 Add proper tutorials | [105](https://github.com/laminlabs/nbproject/pull/105) | [falexwolf](https://github.com/falexwolf) | 2022-06-29 |
📝 Prototype the `nbproject.publish` workflow | [103](https://github.com/laminlabs/nbproject/pull/103) | [falexwolf](https://github.com/falexwolf) | 2022-06-29 |
✨ Take into account packages from store for live dependencies | [104](https://github.com/laminlabs/nbproject/pull/104) | [Koncopd](https://github.com/Koncopd) | 2022-06-29 |
✨ Add field `version` and display live dependencies in header | [102](https://github.com/laminlabs/nbproject/pull/102) | [falexwolf](https://github.com/falexwolf) | 2022-06-29 |
👷 Update coverage CI setup | [101](https://github.com/laminlabs/nbproject/pull/101) | [falexwolf](https://github.com/falexwolf) | 2022-06-26 |
👷 Integrate Codecov to CI | [100](https://github.com/laminlabs/nbproject/pull/100) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-26 |
📝 Re-organize API documentation and clean up guides | [97](https://github.com/laminlabs/nbproject/pull/97) | [falexwolf](https://github.com/falexwolf) | 2022-06-24 | 0.1.0
♻️ Restructure dev submodule | [93](https://github.com/laminlabs/nbproject/pull/93) | [Koncopd](https://github.com/Koncopd) | 2022-06-23 | 0.1a3
🐛 Fix the case when a notebook filename is specified | [94](https://github.com/laminlabs/nbproject/pull/94) | [Koncopd](https://github.com/Koncopd) | 2022-06-23 | 0.1a2
♻️ Re-design package and introduce large parts of the API | [90](https://github.com/laminlabs/nbproject/pull/90) | [Koncopd](https://github.com/Koncopd) | 2022-06-21 | 0.1a1
🧑‍💻 Make CLI `--deps` infer versions by default | [87](https://github.com/laminlabs/nbproject/pull/87) | [Koncopd](https://github.com/Koncopd) | 2022-06-12 |
🩹 Always display dependencies pinned in the metadata | [84](https://github.com/laminlabs/nbproject/pull/84) | [Koncopd](https://github.com/Koncopd) | 2022-06-10 |
💚 Remove server initialization from tests | [83](https://github.com/laminlabs/nbproject/pull/83) | [Koncopd](https://github.com/Koncopd) | 2022-06-09 |
🏗️ Always infer & display dependencies | [80](https://github.com/laminlabs/nbproject/pull/80) | [falexwolf](https://github.com/falexwolf) | 2022-06-08 | 0.0.9
🩹 Fix `meta.title` formatting | [79](https://github.com/laminlabs/nbproject/pull/79) | [falexwolf](https://github.com/falexwolf) | 2022-06-08 |
✨ Expose title in `nbproject.meta` & refactor to loading it dynamically | [77](https://github.com/laminlabs/nbproject/pull/77) | [falexwolf](https://github.com/falexwolf) | 2022-06-08 | 0.0.8
♻️ Rename `meta.uid` to `meta.id` | [75](https://github.com/laminlabs/nbproject/pull/75) | [falexwolf](https://github.com/falexwolf) | 2022-06-08
✨ Infer dependencies on header import | [65](https://github.com/laminlabs/nbproject/pull/65) | [Koncopd](https://github.com/Koncopd) | 2022-06-07 |
🏗️ Access metadata through API | [59](https://github.com/laminlabs/nbproject/pull/59) | [falexwolf](https://github.com/falexwolf) | 2022-06-06 |
✨ Upon interactive init, auto-restart & run | [57](https://github.com/laminlabs/nbproject/pull/57) | [falexwolf](https://github.com/falexwolf) | 2022-06-04 |
♻️ Replace nbformat with orjson everywhere | [50](https://github.com/laminlabs/nbproject/pull/50) | [Koncopd](https://github.com/Koncopd) | 2022-05-31 |
⚡ Improve runtime for `nbproject.header` | [47](https://github.com/laminlabs/nbproject/pull/47) | [Koncopd](https://github.com/Koncopd) | 2022-05-23 |
♻️ Proper treatment of jupyter magic commands | [48](https://github.com/laminlabs/nbproject/pull/48) | [Koncopd](https://github.com/Koncopd) | 2022-05-23 |
💚 Safer pytest run | [41](https://github.com/laminlabs/nbproject/pull/41) | [Koncopd](https://github.com/Koncopd) | 2022-05-15 |
✨ Add dependencies management | [26](https://github.com/laminlabs/nbproject/pull/26) | [Koncopd](https://github.com/Koncopd) | 2022-05-13 |
✨ Project initialization with CLI | [21](https://github.com/laminlabs/nbproject/pull/21) | [Koncopd](https://github.com/Koncopd) | 2022-04-29 |
🎨 Move all jupyter related functionality to one file | [19](https://github.com/laminlabs/nbproject/pull/19) | [Koncopd](https://github.com/Koncopd) | 2022-04-18 |
🏗️ Metadata-aware tests | [9](https://github.com/laminlabs/nbproject/pull/9) | [Koncopd](https://github.com/Koncopd) | 2022-04-07 |
